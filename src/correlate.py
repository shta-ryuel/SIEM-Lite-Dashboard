import sqlite3

def detect_suspicious_logins():
    conn = sqlite3.connect('../siem.db')
    c = conn.cursor()
    alerts = []
    for user in ['alice', 'bob', 'charlie']:
        c.execute("SELECT action FROM logs WHERE user=? ORDER BY timestamp DESC LIMIT 5", (user,))
        actions = [r[0] for r in c.fetchall()]
        if actions.count('login_failed') >= 3 and 'login_success' in actions:
            alerts.append(f"Suspicious login sequence for user {user}")
    conn.close()
    return alerts

def detect_after_hours_file_access():
    conn = sqlite3.connect('../siem.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, user FROM logs WHERE action='file_access'")
    rows = c.fetchall()
    alerts = []
    for ts, user in rows:
        hour = int(ts[11:13])
        if hour < 6 or hour > 20:
            alerts.append(f"{user} accessed file after hours at {ts}")
    conn.close()
    return alerts
