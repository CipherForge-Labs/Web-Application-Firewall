[![CodeQL](https://github.com/CipherForge-Labs/Web-Application-Firewall/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/CipherForge-Labs/Web-Application-Firewall/actions/workflows/github-code-scanning/codeql)
[![Docker Image CI](https://github.com/CipherForge-Labs/Web-Application-Firewall/actions/workflows/docker-image.yml/badge.svg)](https://github.com/CipherForge-Labs/Web-Application-Firewall/actions/workflows/docker-image.yml)
# Web Application Firewall

**Web Application Firewall** (WAF) is a security solution designed to protect web applications from common web attacks such as SQL Injection, Cross-Site Scripting (XSS), and more. This project is built with Python using Flask for the GUI and is easily configurable to suit your web security needs.

### Features
- **SQL Injection Protection**: Detects and blocks SQL injection attempts in web requests.
- **XSS Protection**: Identifies and blocks Cross-Site Scripting (XSS) attacks.
- **IP Blocking**: Block malicious IPs based on attack patterns and behavior.
- **IP Whitelisting**: Allows specific IPs to bypass the firewall.
- **Rate Limiting**: Prevents brute force attacks by limiting the number of requests from a single IP.
- **Logging**: Records blocked requests and attack patterns.
- **Admin Panel**: A simple admin interface to view logs and manage blocked/whitelisted IPs.

### UI Features
- **Login Page**: Secure login with user authentication. Admin users can access the dashboard.
- **Dashboard**: Displays information about the current status of the firewall, recent attacks, and other useful statistics.
- **Logs Page**: View logs of blocked requests and actions taken by the firewall.
- **IP Management**: Add or remove IP addresses from the blocked or whitelisted lists.
- **Onboarding Setup**: When accessing the firewall for the first time, an onboarding setup process is triggered to create the admin password and configure initial settings.

---

## Installation

### Method 1: **Using Docker**

This method provides an easy way to set up the firewall in an isolated environment. It uses Docker to containerize the application.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CipherForge-Labs/Web-Application-Firewall.git
   cd Web-Application-Firewall
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t waf .
   ```

3. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 waf
   ```

   The firewall will be accessible at `http://localhost:5000`.

4. **Stopping the Docker container**:
   ```bash
   docker stop <container_id>
   ```

### Method 2: **Manual Installation (Using Python)**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CipherForge-Labs/Web-Application-Firewall.git
   cd Web-Application-Firewall
   ```

2. **Run the setup script**:
   This script will install the necessary dependencies and set up the environment.
   ```bash
   ./setup.sh
   ```

3. **Run the application**:
   After installation, you can start the Flask web application:
   ```bash
   python3 app.py
   ```

   The firewall will be accessible at `http://localhost:5000`.

### Method 3: **Using Executable (If Available)**

For users who prefer not to install Python or use Docker, an executable version may be provided. To run it:

1. **Download the executable** from the release section of the repository.
2. **Run the executable**:
   Simply run the `.exe` file (on Windows) or the appropriate executable for your OS.
   
   The firewall UI should open in your browser.

---

## Usage

### First-time Setup
When you access the firewall for the first time, you will be prompted to complete an **onboarding setup**. This setup will ask you to create an admin password and configure initial settings such as the IP blocking/whitelisting rules.

1. **Access the firewall** at `http://localhost:5000`.
2. **Complete the onboarding form** by entering the required details.
3. Once completed, you'll be directed to the login page.

### Logging In
After the onboarding setup, you can log in using the credentials created during the setup process.

1. Navigate to `http://localhost:5000/login`.
2. Enter your **admin password** and submit.
3. Upon successful login, you will be directed to the **Dashboard**.

### Managing the WAF
On the **Dashboard**, you can:
- View the firewall status (active, blocked requests, etc.).
- Monitor recent detected attacks (e.g., SQL Injection or XSS).
- Manage IP addresses by blocking or whitelisting them.

To block or whitelist an IP:
1. Navigate to the **IP Management** section.
2. Enter the IP address and choose whether to **Block** or **Whitelist**.

### Viewing Logs
On the **Logs** page, you can view:
- A detailed log of blocked requests.
- Timestamp, IP address, action taken (blocked/whitelisted), and attack type (if detected).

### Rate Limiting
The WAF includes basic rate-limiting features to prevent brute force attacks by limiting the number of requests from a single IP address.

---

## Configuration
The configuration for blocked and whitelisted IPs, as well as attack detection rules, is stored in the following files:

- **waf_logs.json**: Stores the log data of blocked requests and actions.
- **waf_rules.json**: Stores the current rules for blocking/whitelisting IPs and attack detection patterns.

---

## How the WAF Works

1. **Request Filtering**: When a request is made, the WAF inspects it for known attack patterns like SQL Injection and XSS.
2. **Blocking Malicious Requests**: If an attack is detected, the request is blocked, and the IP is logged in `waf_logs.json`. The IP is also added to the blocked IP list in `waf_rules.json`.
3. **IP Management**: Admins can manually block or whitelist IP addresses via the UI, and these changes are reflected in the `waf_rules.json`.
4. **Logging**: Every blocked request and admin action is logged, allowing administrators to keep track of all activities.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

Made with ❤️ by CipherForge Labs
