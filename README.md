# SystemAdmin Toolkit - Log Anomaly Detection Dashboard

![Project Banner](docs/banner.png) <!-- optional banner image -->

## 1. Project Overview
The **SystemAdmin Toolkit** is a web-based dashboard that allows system administrators and cybersecurity professionals to monitor server logs for anomalies in real-time.  
This project leverages **LogAI** to parse, vectorize, and analyze log data, detecting abnormal events that may indicate system misconfigurations, errors, or potential security threats.

**Key Features:**
- Parses Ubuntu Apache `error.log` files.
- Applies feature extraction and anomaly detection.
- Displays results in an interactive dashboard with modern UI styling.
- Provides easy-to-read summaries and anomaly indicators.

---

## 2. Project Relevance
Analyzing system logs for anomalies is crucial in **cybersecurity** and **forensics**:
- Detect unauthorized access attempts, software failures, and configuration errors.
- Early detection of suspicious activities can prevent data breaches.
- Helps IT teams maintain server reliability and compliance.

**Why this project?**
- Provides hands-on experience with log preprocessing, feature extraction, and anomaly detection.
- Explores the application of machine learning in real-world system monitoring.
- Develops skills in Python, Flask, Pandas, and modern UI design.

---

## 3. Methodology

### Setup & Environment
- Follow below steps to set up python environment 

```bash
# Create virtual environment
sudo apt install git python3 apache2 python3.12-venv
# inside repo systemadmin-toolkit/
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

- Run set up script 
```sudo sh setup```

## 4. Results

## 5. Conclusion
