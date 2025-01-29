import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
import urllib.parse
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_only_for_development"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def get_unread_message_count():
    if not current_user.is_authenticated:
        return 0
    from models import Message
    return Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()

app.jinja_env.globals.update(get_unread_message_count=get_unread_message_count)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        from models import User
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    from models import Truck, Message
    trucks = Truck.query.filter_by(user_id=current_user.id).all()
    active_trucks = len([t for t in trucks if t.status == 'active'])
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    return render_template('dashboard.html', 
                         trucks=trucks,
                         active_trucks=active_trucks,
                         truck_count=len(trucks),
                         unread_count=unread_messages)

@app.route('/messages')
@login_required
def messages():
    from models import Message
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', messages=received_messages)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

from flask import jsonify

@app.route('/api/messages/<int:message_id>')
@login_required
def get_message(message_id):
    from models import Message
    message = Message.query.get_or_404(message_id)

    if message.receiver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'subject': message.subject,
        'sender': message.sender.username,
        'timestamp': message.timestamp.strftime('%m/%d/%Y %H:%M'),
        'content': message.content,
        'is_read': message.is_read,
        'truck': f"{message.related_truck.plate_number} - {message.related_truck.driver_name}" if message.related_truck else None
    })

@app.route('/api/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    from models import Message
    message = Message.query.get_or_404(message_id)

    if message.receiver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return jsonify({'status': 'success'})

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    from models import Message

    receiver_id = request.form.get('receiver_id')
    subject = request.form.get('subject')
    content = request.form.get('content')
    related_truck_id = request.form.get('related_truck_id')
    message_type = request.form.get('message_type', 'normal')

    if not all([receiver_id, subject, content]):
        flash('All required fields must be filled out.', 'error')
        return redirect(url_for('messages'))

    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        subject=subject,
        content=content,
        related_truck_id=related_truck_id if related_truck_id else None,
        message_type=message_type
    )

    db.session.add(message)
    db.session.commit()

    flash('Message sent successfully.', 'success')
    return redirect(url_for('messages'))

@app.context_processor
def utility_processor():
    def get_users_for_messaging():
        from models import User
        return User.query.filter(User.id != current_user.id).all()

    def get_user_trucks():
        from models import Truck
        return Truck.query.filter_by(user_id=current_user.id).all()

    return dict(users=get_users_for_messaging, trucks=get_user_trucks)


@app.route('/trucks/<int:truck_id>')
@login_required
def truck_detail(truck_id):
    from models import Truck
    truck = Truck.query.get_or_404(truck_id)
    if truck.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('truck_detail.html', truck=truck)

@app.route('/api/make_call/<int:truck_id>', methods=['POST'])
@login_required
def make_call(truck_id):
    try:
        from models import Truck
        truck = Truck.query.get_or_404(truck_id)

        # Verify truck belongs to current user
        if truck.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Format the phone number to E.164 format
        to_number = request.json.get('to_number')
        if not to_number:
            app.logger.error("No phone number provided")
            return jsonify({
                'status': 'error',
                'message': 'Phone number is required'
            }), 400

        if not to_number.startswith('+'):
            to_number = '+1' + to_number  # Assuming US numbers

        app.logger.info(f"Initiating call to {to_number} for truck {truck_id}")

        # Initialize Twilio client
        client = Client(
            os.environ.get('TWILIO_ACCOUNT_SID'),
            os.environ.get('TWILIO_AUTH_TOKEN')
        )

        # Get the base URL for the voice endpoint
        base_url = request.url_root.rstrip('/')
        if request.is_secure:
            base_url = base_url.replace('http://', 'https://')

        # Make the call using our voice endpoint
        call = client.calls.create(
            url=f"{base_url}/voice",  # Our TwiML endpoint
            to=to_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER')
        )

        app.logger.info(f"Call initiated successfully with SID: {call.sid}")

        return jsonify({
            'status': 'success',
            'call_sid': call.sid,
            'message': f'Initiating call to driver of truck {truck.plate_number}'
        })

    except TwilioRestException as e:
        app.logger.error(f"Twilio error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to initiate call. Please try again.'
        }), 500
    except Exception as e:
        app.logger.error(f"Error making call: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }), 500

def generate_elevenlabs_audio(text):
    """Generate audio using ElevenLabs API"""
    try:
        ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")
        if not ELEVEN_LABS_API_KEY:
            app.logger.error("ElevenLabs API key is missing")
            return None

        VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }

        app.logger.debug(f"Making request to ElevenLabs API with text: {text}")
        app.logger.debug(f"Using ElevenLabs API key: {ELEVEN_LABS_API_KEY[:4]}...")
        app.logger.debug(f"Request URL: {url}")
        app.logger.debug(f"Request headers: {headers}")

        response = requests.post(url, json=data, headers=headers)
        app.logger.debug(f"ElevenLabs API response status: {response.status_code}")

        if response.status_code != 200:
            app.logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None

        # Save the audio file in the static folder
        static_folder = os.path.join(app.root_path, 'static', 'audio')
        os.makedirs(static_folder, exist_ok=True)

        audio_filename = f"temp_audio_{hash(text)}.mp3"
        audio_path = os.path.join(static_folder, audio_filename)

        with open(audio_path, "wb") as f:
            f.write(response.content)

        # Verify the file was created and has content
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            app.logger.debug(f"Audio file created successfully at {audio_path}")
            audio_url = f"audio/{audio_filename}"
            app.logger.debug(f"Returning audio URL: {audio_url}")
            return audio_url
        else:
            app.logger.error("Failed to create audio file or file is empty")
            return None

    except Exception as e:
        app.logger.error(f"Error generating ElevenLabs audio: {str(e)}")
        app.logger.exception("Full traceback:")
        return None

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    """Handle incoming voice calls with ElevenLabs integration."""
    try:
        app.logger.info("Voice endpoint called")
        app.logger.info(f"Request method: {request.method}")
        app.logger.info(f"Request values: {request.values}")

        resp = VoiceResponse()

        if 'SpeechResult' in request.values:
            speech_text = request.values['SpeechResult']
            app.logger.info(f"Received speech: {speech_text}")

            # Generate response using ElevenLabs
            response_text = "I received your message. Let me help you with that."
            audio_file = generate_elevenlabs_audio(response_text)

            if audio_file:
                # Generate a full URL for the audio file
                audio_url = request.url_root.rstrip('/') + url_for('static', filename=audio_file)
                app.logger.info(f"Playing audio from URL: {audio_url}")
                resp.play(audio_url)
            else:
                app.logger.warning("ElevenLabs audio generation failed, falling back to Twilio voice")
                resp.say(response_text, voice='alice')

            # Set up for next input
            gather = Gather(
                input='speech',
                action='/voice',
                method='POST',
                timeout=3,
                speechTimeout='auto'
            )

            # Generate follow-up prompt
            follow_up_text = "Please continue with your question or request about fleet management."
            follow_up_audio = generate_elevenlabs_audio(follow_up_text)

            if follow_up_audio:
                gather.play(request.url_root.rstrip('/') + url_for('static', filename=follow_up_audio))
            else:
                gather.say(follow_up_text, voice='alice')

            resp.append(gather)
        else:
            # Initial greeting
            welcome_text = "Hello, I'm your AI Fleet Assistant powered by ElevenLabs. I'm here to help you manage your truck fleet efficiently. How may I assist you today?"
            audio_file = generate_elevenlabs_audio(welcome_text)

            if audio_file:
                audio_url = request.url_root.rstrip('/') + url_for('static', filename=audio_file)
                app.logger.info(f"Playing welcome audio from URL: {audio_url}")
                resp.play(audio_url)
            else:
                app.logger.warning("Initial ElevenLabs audio generation failed, falling back to Twilio voice")
                resp.say(welcome_text, voice='alice')

            gather = Gather(
                input='speech',
                action='/voice',
                method='POST',
                timeout=3,
                speechTimeout='auto'
            )
            resp.append(gather)

        app.logger.info("Voice response created successfully")
        app.logger.info(f"Response TwiML: {str(resp)}")
        return str(resp)

    except Exception as e:
        app.logger.error(f"Error in voice endpoint: {str(e)}")
        app.logger.exception("Full traceback:")
        error_response = VoiceResponse()
        error_text = "I apologize, but I encountered an error. Please try again."
        error_audio = generate_elevenlabs_audio(error_text)

        if error_audio:
            error_response.play(request.url_root.rstrip('/') + url_for('static', filename=error_audio))
        else:
            error_response.say(error_text, voice='alice')

        return str(error_response)

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files with correct content type"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'audio'),
        filename,
        mimetype='audio/mpeg'
    )

with app.app_context():
    # Import models after app creation to avoid circular imports
    from models import User, Truck, Message
    db.create_all()

    def create_admin_user():
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                logging.info("Admin user created successfully")
            else:
                logging.info("Admin user already exists")
        except Exception as e:
            logging.error(f"Error creating admin user: {e}")
            db.session.rollback()

    create_admin_user()