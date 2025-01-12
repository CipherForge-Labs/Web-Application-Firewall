import json
import re
from datetime import datetime

# Load rules from JSON files
def load_rules():
    try:
        with open('waf_rules.json', 'r') as rules_file:
            return json.load(rules_file)
    except FileNotFoundError:
        # If the file doesn't exist, return empty rules
        return {"blocked_ips": [], "whitelisted_ips": []}

# Save rules to JSON file
def save_rules(rules):
    with open('waf_rules.json', 'w') as rules_file:
        json.dump(rules, rules_file, indent=4)

# Load logs from JSON file
def load_logs():
    try:
        with open('waf_logs.json', 'r') as log_file:
            return json.load(log_file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

# Save logs to JSON file
def save_logs(logs):
    with open('waf_logs.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)

# Log activities
def log_activity(ip_address, action, details):
    logs = load_logs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = {
        "timestamp": timestamp,
        "ip_address": ip_address,
        "action": action,
        "details": details
    }
    logs.append(log_data)
    save_logs(logs)

# Check for SQL Injection attack
def detect_sql_injection(request_data):
    sql_patterns = [
        r"(\b(select|insert|delete|update|drop|create|alter|grant|revoke)\b)",
        r"(--|\bunion\b|\bselect\b|\binsert\b|\bdrop\b|\bupdate\b|\bdelete\b|\bcreate\b|\bshow\b)"
    ]
    for pattern in sql_patterns:
        if re.search(pattern, request_data, re.IGNORECASE):
            return True
    return False

# Check for Cross-Site Scripting (XSS) attack
def detect_xss(request_data):
    xss_patterns = [
        r"<script.*?>.*?</script.*?>",  # Basic XSS patterns
        r"(<img.*?src\s*=\s*['\"]*.*?javascript:.*?)"
    ]
    for pattern in xss_patterns:
        if re.search(pattern, request_data, re.IGNORECASE):
            return True
    return False

# Block an IP if it is detected as malicious
def block_ip(ip_address):
    rules = load_rules()
    if ip_address not in rules["blocked_ips"]:
        rules["blocked_ips"].append(ip_address)
        save_rules(rules)
        log_activity(ip_address, "Blocked", "IP detected for malicious activity")

# Whitelist an IP
def whitelist_ip(ip_address):
    rules = load_rules()
    if ip_address in rules["blocked_ips"]:
        rules["blocked_ips"].remove(ip_address)
    if ip_address not in rules["whitelisted_ips"]:
        rules["whitelisted_ips"].append(ip_address)
        save_rules(rules)
        log_activity(ip_address, "Whitelisted", "IP manually whitelisted by admin")

# Main WAF detection function
def waf_filter(request_data, ip_address):
    rules = load_rules()

    # Check if the IP is whitelisted or blocked
    if ip_address in rules["whitelisted_ips"]:
        return "IP is whitelisted, no action needed."
    elif ip_address in rules["blocked_ips"]:
        return "IP is blocked, request denied."

    # Check for SQL Injection
    if detect_sql_injection(request_data):
        log_activity(ip_address, "Blocked", "SQL Injection detected")
        block_ip(ip_address)
        return "SQL Injection detected, request blocked."

    # Check for XSS
    if detect_xss(request_data):
        log_activity(ip_address, "Blocked", "XSS Attack detected")
        block_ip(ip_address)
        return "XSS Attack detected, request blocked."

    # If no attacks are detected, allow the request
    return "Request allowed."

# Example usage of the WAF filter
if __name__ == "__main__":
    # Sample incoming request data
    request_data = "<script>alert('XSS')</script>"
    ip_address = "192.168.1.1"

    result = waf_filter(request_data, ip_address)
    print(result)  # This will print the result of the request filter (blocked/allowed)

