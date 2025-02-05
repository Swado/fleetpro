from app import app
import routes  # Add this import to ensure routes are registered
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)