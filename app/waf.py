"""
Web Application Firewall (WAF) functionality for handling requests and managing IP blocking.
"""

import os
import json
from flask import request, Flask

# Initialize Flask app
app = Flask(__name__)

# Function to load the current rules from a file
def load_rules():
    """
    Load the firewall rules from a file.
    """
    if os.path.exists("rules.json"):
        with open("rules.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Function to save the current rules to a file
def save_rules(rules):
    """
    Save the firewall rules to a file.
    """
    with open("rules.json", "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=4)

# Function to block an IP address
def block_ip(ip_address):
    """
    Block an IP address by adding it to the rules.
    """
    rules = load_rules()
    rules.append({"ip": ip_address, "action": "block"})
    save_rules(rules)

# Function to unblock an IP address
def unblock_ip(ip_address):
    """
    Unblock an IP address by removing it from the rules.
    """
    rules = load_rules()
    rules = [rule for rule in rules if rule["ip"] != ip_address]
    save_rules(rules)

# Function to analyze requests and detect malicious behavior
def analyze_request(request_data):
    """
    Analyze a request and determine if it is malicious.
    For simplicity, this function detects SQL Injection and XSS.
    """
    if "DROP TABLE" in request_data or "UNION SELECT" in request_data:
        return True  # SQL Injection detected
    if "<script>" in request_data or "</script>" in request_data:
        return True  # XSS detected
    return False

# Function to handle incoming requests and block if malicious
def handle_request():
    """
    Handle the incoming request, analyze it, and block the IP if malicious.
    """
    request_data = request.data.decode("utf-8")  # Get the request data
    if analyze_request(request_data):
        ip_address = request.remote_addr
        block_ip(ip_address)
        return "Request blocked due to malicious content", 403
    return "Request allowed", 200

# Route for handling incoming requests
@app.route('/waf', methods=['POST'])
def waf_route():
    """
    Handle the incoming request at /waf route.
    This route processes the request data, checks for malicious behavior, 
    and blocks the IP if necessary.
    """
    # Example: Getting request data (could be headers, body, etc.)
    request_data = request.get_json()
    
    # Analyze the request for malicious behavior
    result = analyze_request(request_data)
    
    if result.get('action') == 'block':
        ip_address = result.get('ip')
        block_ip(ip_address)
        return {"message": f"IP {ip_address} blocked due to malicious behavior."}, 403
    elif result.get('action') == 'unblock':
        ip_address = result.get('ip')
        unblock_ip(ip_address)
        return {"message": f"IP {ip_address} unblocked."}, 200
    else:
        return {"message": "Request is clean."}, 200


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
