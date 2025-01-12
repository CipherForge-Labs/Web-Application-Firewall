from flask import Flask, request, jsonify

def init_app():
    """
    Initialize the Flask application by loading configurations and setting up routes.
    """
    app = Flask(__name__)

    # Load configurations
    load_config(app)

    # Setup routes
    setup_routes(app)

    return app

def load_config(app):
    """
    Load configuration settings for the Flask app (e.g., from environment variables or files).
    """
    # Example: loading configurations from a config.py file
    try:
        app.config.from_pyfile('config.py')  # Ensure you have a config.py or adjust path accordingly
    except Exception as e:
        print(f"Error loading config: {e}")
    
    # You can also manually set configurations like:
    # app.config['DEBUG'] = True  # Set debug mode directly if not using a config file

def setup_routes(app):
    """
    Define the application's route functions.
    """
    @app.route('/')
    def home():
        """
        Home route.
        """
        return "Welcome to the home page!"

    @app.route('/waf', methods=['POST'])
    def waf_route():
        """
        Handle incoming requests at the /waf route.
        This function analyzes the request and applies WAF rules.
        """
        request_data = request.get_json()  # Assuming JSON data is sent
        if request_data:
            action = analyze_request(request_data)
            return jsonify({"action": action}), 200
        return jsonify({"error": "Invalid data"}), 400

def analyze_request(request_data):
    """
    Analyze a request and determine if it is malicious.
    For simplicity, this function detects SQL Injection and XSS.
    """
    if detect_sql_injection(request_data):
        return "block"
    if detect_xss(request_data):
        return "block"
    return "allow"

def detect_sql_injection(request_data):
    """
    Simple SQL Injection detection (could be enhanced).
    """
    sql_keywords = ["' OR", "'--", "';--", "DROP TABLE", "SELECT * FROM", "INSERT INTO"]
    for keyword in sql_keywords:
        if keyword.lower() in str(request_data).lower():
            return True
    return False

def detect_xss(request_data):
    """
    Simple XSS detection (could be enhanced).
    """
    xss_keywords = ["<script>", "</script>", "<img src=", "onerror="]
    for keyword in xss_keywords:
        if keyword.lower() in str(request_data).lower():
            return True
    return False

# Entry point to start the application (typically placed in a separate file like run.py)
if __name__ == '__main__':
    app = init_app()
    app.run(debug=True)
