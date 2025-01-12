from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Dummy initial data for the example
# In a real application, use a database for storing users, logs, and other data
users = {
    "admin": generate_password_hash("admin123")  # Replace with the real admin password
}

blocked_ips = set()  # Example: Set to store blocked IPs
whitelisted_ips = set()  # Example: Set to store whitelisted IPs
logs = []  # List to store logs (usually a database)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username exists and the password is correct
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/admin_panel')
def admin_panel():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin_panel.html', logged_in=True, setup_incomplete=False)

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            # Store the password (in reality, store this in a secure database)
            users['admin'] = generate_password_hash(password)
            return redirect(url_for('login'))
        else:
            return render_template('onboarding.html', error="Passwords do not match")
    return render_template('onboarding.html')

@app.route('/block_ip', methods=['POST'])
def block_ip():
    ip_address = request.form['ip_address']
    blocked_ips.add(ip_address)
    logs.append({'timestamp': '2025-01-12', 'ip_address': ip_address, 'action': 'Blocked', 'details': 'IP Blocked by Admin'})
    return redirect(url_for('admin_panel'))

@app.route('/whitelist_ip', methods=['POST'])
def whitelist_ip():
    ip_address = request.form['ip_address']
    if ip_address in blocked_ips:
        blocked_ips.remove(ip_address)
    whitelisted_ips.add(ip_address)
    logs.append({'timestamp': '2025-01-12', 'ip_address': ip_address, 'action': 'Whitelisted', 'details': 'IP Whitelisted by Admin'})
    return redirect(url_for('admin_panel'))

@app.route('/logs')
def view_logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('logs.html', logs=logs)

@app.route('/set_rate_limit', methods=['POST'])
def set_rate_limit():
    rate_limit = request.form['rate_limit']
    # Here you can implement rate-limiting logic based on `rate_limit`
    logs.append({'timestamp': '2025-01-12', 'ip_address': 'N/A', 'action': 'Rate Limit Set', 'details': f'Set to {rate_limit} requests per minute'})
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
