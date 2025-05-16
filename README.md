Insider Threat Detection System (ITDS)

A machine learning-based real-time insider threat detection system that analyzes user behavior, classifies potential threats, and provides an interactive dashboard for monitoring.

Table of Contents
Overview
Features
Installation
Usage
Dataset
Methodology
Contributors
Future Work
License

Overview
Insider threats pose significant challenges to organizational cybersecurity. This project addresses these challenges by developing a real-time monitoring system using machine learning (Random Forest classifier) and Streamlit for visualization. The system processes user activity logs, detects suspicious behavior, and displays alerts via an interactive dashboard.

Features
Real-time Monitoring: Processes and analyzes user activity data in real-time.
Interactive Dashboard: Built with Streamlit, featuring:
Live threat cards (color-coded by severity)
Historical trend analysis (Plotly graphs)
Dark/light mode toggle
Machine Learning Pipeline:
Data preprocessing and feature engineering
Random Forest classifier for threat detection
SHAP values for model explainability

Simulation Tool: simulate_realtime.py generates test data for real-time testing.

Installation
Clone the repository:
git clone https://github.com/IT22361486/insider_threat_detector.git
cd insider-threat-detection

Set up a Python virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Download the CERT Insider Threat Dataset r1 and place the files (logon.csv, device.csv, http.csv) in the data/raw folder.

Usage
Preprocess the data:
python src/preprocessing.py

Train the model:
python src/train_model.py

Run the Streamlit dashboard:
streamlit run src/dashboard.py

Simulate real-time data (optional, for testing):
python src/simulate_realtime.py

Dataset
The project uses the CERT Insider Threat Dataset r1 from Carnegie Mellon University, which includes:
logon.csv: User login/logout timestamps.
device.csv: USB/hardware usage logs.
http.csv: Web activity logs.

Methodology
Data Preprocessing: Cleaned and normalized raw logs, extracted features (e.g., login counts, device connections).
Threat Labeling: Applied rule-based labeling (e.g., logins > 5 → Warning).
Model Training: Trained a Random Forest classifier on the labeled data.
Real-time Detection: Simulated live data streams for testing.
Dashboard: Visualized results using Streamlit and Plotly.

Contributors
Herath H. M. G. D. K. (IT22361486) - Project Lead
Responsibilities: Data preprocessing, model development, dashboard design.

De Alwis H. P. G. H. S. (IT22317926) - Technical Lead
Responsibilities: Dashboard development, testing, and simulation.

Future Work
Integration with SIEM tools (e.g., Splunk, ELK).
Deep learning models (LSTM, autoencoders) for behavior analysis.
Multi-user authentication for the dashboard.
Adaptive labeling using unsupervised anomaly detection.

License
This project is licensed under the MIT License. See the LICENSE file for details.

For questions or feedback, please open an issue or contact the contributors.
Submission Date: 14/05/2025
Institution: Sri Lanka Institute of Information Technology
Module: Information Security Project (IE3092)
