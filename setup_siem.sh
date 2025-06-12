#!/bin/bash

echo "🔐 Setting up SIEM-lite Project..."

# Step 1: Create folders
mkdir -p siem-lite/logs
mkdir -p siem-lite/src
cd siem-lite

touch siem.db

# Step 2: Create Python files
cat << EOF > src/generate_logs.py
import csv
import random
from datetime import datetime, timedelta

users = ['alice', 'bob', 'charlie']
actions = ['login_failed', 'login_success', 'file_access', 'logout']

with open('../logs/sample_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'user', 'action'])
    now = datetime.now()
    for _ in range(200):
        user = random.choice(users)
        action = random.choice(actions)
        ts = now - timedelta(minutes=random.randint(0, 1000))
        writer.writerow([ts.isoformat(), user, action])
EOF

cat << EOF > src/load_logs.py
import sqlite3
import csv

def create_db():
    conn = sqlite3.connect('../siem.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                user TEXT,
                action TEXT)''')
    conn.commit()
    conn.close()

def insert_logs():
    conn = sqlite3.connect('../siem.db')
    c = conn.cursor()
    with open('../logs/sample_logs.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute("INSERT INTO logs (timestamp, user, action) VALUES (?, ?, ?)",
                      (row['timestamp'], row['user'], row['action']))
    conn.commit()
    conn.close()

create_db()
insert_logs()
EOF

cat << EOF > src/correlate.py
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
EOF

cat << EOF > src/dashboard.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from correlate import detect_suspicious_logins, detect_after_hours_file_access

st.set_page_config(page_title="SIEM-Lite Dashboard", layout="wide")
st.title("SIEM-Lite Dashboard")

conn = sqlite3.connect('../siem.db')
df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
conn.close()

search = st.text_input("Search logs by username or action")
if search:
    df = df[df.apply(lambda row: search.lower() in row['user'].lower() or search.lower() in row['action'].lower(), axis=1)]

st.subheader("All Logs")
st.dataframe(df, use_container_width=True)

st.subheader("Suspicious Alerts")
alerts = detect_suspicious_logins() + detect_after_hours_file_access()
if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No suspicious activity detected.")

st.subheader("Logins per User")
login_counts = df[df['action'].str.contains("login")].groupby('user')['action'].count()
fig, ax = plt.subplots()
login_counts.plot(kind='bar', ax=ax)
st.pyplot(fig)

st.subheader("Export Alerts")
if alerts:
    if st.button("Download Alerts as CSV"):
        alert_df = pd.DataFrame(alerts, columns=['Alert'])
        alert_df.to_csv("alerts.csv", index=False)
        st.success("alerts.csv saved!")
EOF

# Step 3: Install dependencies
echo "📦 Installing Python libraries..."
pip3 install streamlit pandas matplotlib

# Step 4: Generate logs and load into DB
echo "⚙️ Generating and loading logs..."
cd src
python3 generate_logs.py
python3 load_logs.py

# Step 5: Launch dashboard
echo "🌐 Launching Streamlit dashboard..."
streamlit run dashboard.py

