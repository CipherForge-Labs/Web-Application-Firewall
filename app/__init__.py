from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)

# Password storage location
PASSWORD_FILE = "admin_password.txt"

# Check if the password file exists; if not, create one
if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "w") as f:
        f.write(generate_password_hash("admin123"))

# Function to load the admin password hash from the file
def get_admin_password():
    with open(PASSWORD_FILE, "r") as f:
        return f.read().strip()

# Function to verify password
def verify_password(password):
    return check_password_hash(get_admin_password(), password)

# Load WAF rules from a JSON file
def load_rules():
    if os.path.exists("rules.json"):
        with open("rules.json", "r") as f:
            return json.load(f)
    return []

# Save WAF rules to a JSON file
def save_rules(rules):
    with open("rules.json", "w") as f:
        json.dump(rules, f, indent=4)

# Function to add IP to the blacklist
def block_ip(ip_address):
    rules = load_rules()
    rules.append({"ip": ip_address, "action": "block"})
    save_rules(rules)

# Function to unblock an IP
def unblock_ip(ip_address):
    rules = load_rules()
    rules = [rule for rule in rules if rule["ip"] != ip_address]
    save_rules(rules)

# Endpoint for blocking IP
@app.route("/block_ip", methods=["POST"])
def block_ip_endpoint():
    ip_address = request.form.get("ip_address")
    if ip_address:
        block_ip(ip_address)
        return jsonify({"message": f"IP {ip_address} blocked successfully!"}), 200
    return jsonify({"error": "IP address is required!"}), 400

# Endpoint for unblocking IP
@app.route("/unblock_ip", methods=["POST"])
def unblock_ip_endpoint():
    ip_address = request.form.get("ip_address")
    if ip_address:
        unblock_ip(ip_address)
        return jsonify({"message": f"IP {ip_address} unblocked successfully!"}), 200
    return jsonify({"error": "IP address is required!"}), 400

# Endpoint for login (admin)
@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password")
    if verify_password(password):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid password!"}), 401

# Default route
@app.route("/")
def home():
    return "Welcome to the Web Application Firewall!"

if __name__ == "__main__":
    app.run(debug=True)
