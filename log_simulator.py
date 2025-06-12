import time
import random
from datetime import datetime
import os

# Create log directory if not exists
os.makedirs("logs", exist_ok=True)

log_file_path = "logs/security.log"

log_sources = ["Firewall", "WebServer", "Endpoint", "VPN", "AuthSystem"]
log_actions = [
    "ALLOW",
    "DENY",
    "LOGIN_SUCCESS",
    "LOGIN_FAILURE",
    "FILE_ACCESSED",
    "PORT_SCAN_DETECTED",
    "MALWARE_DETECTED",
    "VPN_CONNECTED",
    "VPN_DISCONNECTED",
    "PRIV_ESC_ATTEMPT"
]

users = ["alice", "bob", "charlie", "admin", "eve"]

def generate_log():
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    source = random.choice(log_sources)
    action = random.choice(log_actions)
    user = random.choice(users)
    ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    return f"{timestamp} | {source} | {action} | user={user} | ip={ip}"

def simulate_logs():
    with open(log_file_path, "a") as log_file:
        while True:
            log_entry = generate_log()
            log_file.write(log_entry + "\n")
            log_file.flush()
            print(f"[+] Logged: {log_entry}")
            time.sleep(random.uniform(0.5, 2))  # adjustable delay

if __name__ == "__main__":
    simulate_logs()

