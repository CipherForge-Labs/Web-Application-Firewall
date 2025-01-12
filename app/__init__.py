from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Sample flags for onboarding completion
setup_complete = False  # Change this to True after onboarding is completed

@app.route('/')
def index():
    """
    Redirect root URL to /onboarding if setup is not complete.
    Otherwise, redirect to admin login.
    """
    if not setup_complete:
        return redirect(url_for('onboarding'))
    return redirect(url_for('admin_login'))

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    """
    Handles onboarding.
    """
    global setup_complete
    if request.method == 'POST':
        # Simulate onboarding completion
        setup_complete = True
        return redirect(url_for('admin_login'))
    return render_template('onboarding.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """
    Handles admin login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simulate login (replace with real authentication logic)
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        return "Invalid credentials", 401
    return render_template('admin_login.html')

@app.route('/admin-panel')
def admin_panel():
    """
    Admin panel after successful login.
    """
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_panel.html')

def setup_app():
    """
    Setup function for initializing the app.
    """
    # Additional setup code if needed
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
