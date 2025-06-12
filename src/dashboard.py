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
