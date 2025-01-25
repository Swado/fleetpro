import os
import pickle
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import logging

class GmailService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.service = None
        self.creds = None
        self.REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:5000/oauth2callback')

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        try:
            # Token file path
            token_file = 'token.pickle'
            client_id = os.environ.get('GMAIL_CLIENT_ID')
            client_secret = os.environ.get('GMAIL_CLIENT_SECRET')

            if not client_id or not client_secret:
                logging.error("Missing Gmail API credentials")
                return False

            # Load existing token
            if os.path.exists(token_file):
                with open(token_file, 'rb') as token:
                    self.creds = pickle.load(token)

            # If credentials are not valid or don't exist, get new ones
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = Flow.from_client_config(
                        {
                            "web": {
                                "client_id": client_id,
                                "client_secret": client_secret,
                                "redirect_uris": [self.REDIRECT_URI],
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token"
                            }
                        },
                        self.SCOPES
                    )
                    flow.redirect_uri = self.REDIRECT_URI
                    auth_url = flow.authorization_url()[0]
                    return auth_url

                # Save the credentials for future use
                with open(token_file, 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('gmail', 'v1', credentials=self.creds)
            logging.info("Gmail service authenticated successfully")
            return True

        except Exception as e:
            logging.error(f"Error authenticating Gmail service: {e}", exc_info=True)
            return False

    def send_email(self, to, subject, body):
        """Send email using Gmail API"""
        try:
            if not self.service:
                if not self.authenticate():
                    raise Exception("Failed to authenticate Gmail service")

            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            # Send the email
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            logging.info(f"Email sent successfully to {to}")
            return True

        except Exception as e:
            logging.error(f"Error sending email: {e}", exc_info=True)
            return False

# Initialize Gmail service
gmail_service = GmailService()