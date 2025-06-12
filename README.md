![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)






### SIEM-lite: Real-Time Security Log Dashboard

A lightweight Security Information and Event Management (SIEM) dashboard built using **Streamlit**. 
It simulates logs from multiple sources and detects key alerts like port scans, login failures, and privilege escalation attempts. 
Designed for cybersecurity beginners to **understand log correlation and alerting** without paid tools.

 ### Features
-  Real-time log ingestion and parsing
-  Alert detection for multi-step threats
-  Dashboard with metrics, top IPs, alert types
-  Filters: user, IP, alert type, keyword search
-  Download filtered logs as CSV
-  Keyword-based rule logic
-  Sleek UI powered by Streamlit

### Preview
![Dashboard Preview](assets/preview.gif)



### Setup Instructions
### 1. Clone this repo
```bash
git clone https://github.com/yourusername/siem-lite-dashboard.git
cd siem-lite-dashboard
```
### 2. Run the log simulator (in one terminal)
```bash
python log_simulator.py
```
### 3. Launch the dashboard (in a second terminal)
```bash
streamlit run dashboard.py
```

### Sample Log Format
```
2025-06-04 21:10:23 | FIREWALL | PORT_SCAN_DETECTED | user=alice | ip=192.168.1.12
```

### Tech Stack
- Python 3
- Streamlit
- Pandas
- Basic Rule-Based Correlation


## Future Ideas
- Add authentication layer
- Log forwarding via syslog
- Time-series line chart for attack spikes
- Deploy to Streamlit Cloud or Heroku
