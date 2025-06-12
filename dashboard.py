import streamlit as st
import pandas as pd
import time
import os

LOG_FILE = "logs/security.log"
MAX_LOGS = 200

st.set_page_config(page_title="SIEM-lite Dashboard", layout="wide")

st.markdown("# 🛡️ SIEM-lite Dashboard")
st.markdown("Real-time log monitoring and alerting for security events.")

# --- Utility Function ---
@st.cache_data(ttl=5)
def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            lines = file.readlines()[-MAX_LOGS:]  # last 200 logs
            data = []
            for line in lines:
                parts = line.strip().split(" | ")
                if len(parts) >= 4:
                    timestamp, source, alert, metadata = parts[0], parts[1], parts[2], " | ".join(parts[3:])
                    data.append((timestamp, source, alert, metadata))
        df = pd.DataFrame(data, columns=["Timestamp", "Source", "Alert Type", "Metadata"])
        return df
    return pd.DataFrame(columns=["Timestamp", "Source", "Alert Type", "Metadata"])

def filter_logs(df, keyword, alert_type, source):
    if keyword:
        df = df[df.apply(lambda row: keyword.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    if alert_type and alert_type != "All":
        df = df[df["Alert Type"] == alert_type]
    if source and source != "All":
        df = df[df["Source"] == source]
    return df

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Filters")
    keyword = st.text_input("Search Keyword")
    df = load_logs()
    alert_options = ["All"] + sorted(df["Alert Type"].unique())
    alert_type = st.selectbox("Alert Type", alert_options)

    source_options = ["All"] + sorted(df["Source"].unique())
    source = st.selectbox("Log Source", source_options)

    auto_refresh = st.checkbox("🔄 Auto-refresh every 5s", value=True)

# --- Filtered Logs ---
filtered_logs = filter_logs(df, keyword, alert_type, source)

# --- Dashboard Stats ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Logs", len(df))
col2.metric("Filtered Logs", len(filtered_logs))
col3.metric("Unique IPs", df['Metadata'].str.extract(r'ip=(\d+\.\d+\.\d+\.\d+)')[0].nunique())

# --- Display Logs ---
st.subheader("📄 Log Viewer")
st.dataframe(filtered_logs, use_container_width=True)

# --- Download Button ---
csv = filtered_logs.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Filtered Logs", data=csv, file_name="filtered_logs.csv", mime="text/csv")

# --- Auto Refresh ---
if auto_refresh:
    time.sleep(5)
    st.rerun()




