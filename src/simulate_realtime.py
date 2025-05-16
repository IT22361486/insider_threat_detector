# src/simulate_realtime.py (Fixed Version)
import random
import time
import joblib
import pandas as pd  # Add this import
from sklearn.utils.validation import check_array  # Add this import

model = joblib.load("data/results/threat_model.pkl")

def predict_threat(logins, devices):
    # Create a DataFrame with proper feature names
    X = pd.DataFrame([[logins, devices]], 
                    columns=['logins_per_day', 'device_connections'])
    return model.predict(X)[0]

while True:
    try:
        logins = random.randint(1, 15)
        devices = random.randint(0, 7)
        
        threat = predict_threat(logins, devices)
        
        if threat == 0:
            status = "\033[92mNormal\033[0m"
        elif threat == 1:
            status = "\033[93mWarning\033[0m"
        else:
            status = "\033[91mCRITICAL\033[0m"
        
        print(f"Logins: {logins:2d} | Devices: {devices} | Status: {status}")
        time.sleep(2)
        
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
        break