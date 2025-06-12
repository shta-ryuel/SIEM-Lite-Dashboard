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
