"""
Web Application Firewall (WAF) module.
This module handles requests and applies basic filtering rules.
"""

import json
from flask import request
import os

# File to store WAF rules
RULES_FILE = "rules.json"

# Function to load rules from the rules file
def load_rules():
    """
    Load WAF rules from a JSON file.
    Returns an empty list if the file does not exist.
    """
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Function to save rules to a JSON file
def save_rules(rules):
    """
    Save WAF rules to a JSON file.
    """
    with open(RULES_FILE, "w", encoding="utf-8") as f:
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
    if "DROP TABLE" in request_data or "SELECT * FROM" in request_data:
        return "SQL Injection detected"
    if "<script>" in request_data or "</script>" in request_data:
        return "XSS detected"
    return "Request is safe"

# Function to handle requests
def handle_request():
    """
    Handle incoming requests and apply WAF rules.
    This function checks the request data and applies filtering rules.
    """
    ip_address = request.remote_addr
    request_data = request.data.decode("utf-8")
    
    # Check if the IP is blocked
    rules = load_rules()
    for rule in rules:
        if rule["ip"] == ip_address and rule["action"] == "block":
            return "Access denied: Your IP is blocked."

    # Analyze the request data for potential threats
    result = analyze_request(request_data)

    # If the request is safe, allow it; otherwise, block it
    if result == "Request is safe":
        return "Request allowed"
    else:
        block_ip(ip_address)
        return f"Access denied: {result}"

# Function to handle login request
def login(request_data):
    """
    Handle login requests.
    Verifies the admin credentials and returns a message.
    """
    password = request_data.get("password")
    if password == "admin123":  # For simplicity, using a hardcoded password
        return "Login successful"
    return "Invalid password"

# Example route: login route
@app.route("/login", methods=["POST"])
def login_route():
    """
    Endpoint for admin login.
    """
    data = request.get_json()
    return login(data)

# Example route: handle requests
@app.route("/request", methods=["POST"])
def request_route():
    """
    Endpoint for handling requests.
    """
    data = request.get_json()
    return handle_request()

if __name__ == "__main__":
    app.run(debug=True)
