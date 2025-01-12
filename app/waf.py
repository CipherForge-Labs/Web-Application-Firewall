from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Constant for setup completion
SETUP_COMPLETE = False  # Changed to uppercase as per PEP8

@app.route('/')
def index():
    """
    Index route that checks if the setup is complete.
    Redirects to the onboarding page if setup is incomplete.
    """
    if not SETUP_COMPLETE:
        return redirect(url_for('onboarding'))
    return redirect(url_for('admin_login'))


@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    """
    Onboarding route where the user sets up the initial admin password.
    Redirects to admin login after setup is completed.
    """
    global SETUP_COMPLETE  # Refactor this if possible to avoid global variable
    if request.method == 'POST':
        # Handle setup form data and complete the setup
        SETUP_COMPLETE = True
        return redirect(url_for('admin_login'))
    return render_template('onboarding.html')


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login route to authenticate users.
    If successful, redirects to the admin panel.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate credentials
        if username == "admin" and password == "password":
            return redirect(url_for('admin_panel'))
        return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')


@app.route('/admin-panel')
def admin_panel():
    """
    Admin panel route where the logged-in admin can manage the firewall.
    """
    return render_template('admin_panel.html', logged_in=True)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/block-ip', methods=['POST'])
def block_ip_route():
    """Route to block an IP address"""
    ip = request.form['ip_to_block']
    block_ip(ip)
    return redirect(url_for('admin_panel'))  # Redirect back to the admin panel

@app.route('/whitelist-ip', methods=['POST'])
def whitelist_ip_route():
    """Route to whitelist an IP address"""
    ip = request.form['ip_to_whitelist']
    whitelist_ip(ip)
    return redirect(url_for('admin_panel'))  # Redirect back to the admin panel
