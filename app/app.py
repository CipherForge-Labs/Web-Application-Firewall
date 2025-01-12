from flask import Flask
from app.waf import waf_route  # Import the WAF route handler from your 'waf.py' file

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Register the WAF route
    app.register_blueprint(waf_route)

    return app

# Initialize the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
