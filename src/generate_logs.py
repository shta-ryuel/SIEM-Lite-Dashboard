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
