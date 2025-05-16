# preprocessing.py - COMPLETE VERSION
import pandas as pd
import os

def process_logons():
    print("Processing logon data...")
    # 1. Read file
    logons = pd.read_csv("data/raw/r1/logon.csv")
    
    # 2. Fix column names if needed
    if logons.columns[0].startswith('{'):
        logons = pd.read_csv("data/raw/r1/logon.csv", header=0)
    
    # 3. Convert date and count logins
    logons['date'] = pd.to_datetime(logons['date'])
    logon_counts = logons[logons['activity'] == 'Logon'].groupby(
        ['user', logons['date'].dt.date]).size().reset_index(name='logins_per_day')
    
    # 4. Save
    os.makedirs("data/processed", exist_ok=True)
    logon_counts.to_csv("data/processed/logon_features.csv", index=False)
    print("Saved logon_features.csv")

def process_devices():
    print("\nProcessing device data...")
    # 1. Read file
    devices = pd.read_csv("data/raw/r1/device.csv")
    
    # 2. Fix column names if needed
    if devices.columns[0].startswith('{'):
        devices = pd.read_csv("data/raw/r1/device.csv", header=0)
    
    # 3. Count device connections
    device_counts = devices[devices['activity'] == 'Connect'].groupby(
        ['user', pd.to_datetime(devices['date']).dt.date]).size().reset_index(name='device_connections')
    
    # 4. Save
    device_counts.to_csv("data/processed/device_features.csv", index=False)
    print("Saved device_features.csv")

def combine_features():
    print("\nCombining features...")
    # 1. Load both files
    logons = pd.read_csv("data/processed/logon_features.csv")
    devices = pd.read_csv("data/processed/device_features.csv")
    
    # 2. Merge them
    combined = pd.merge(logons, devices, on=['user', 'date'], how='left')
    
    # 3. Replace NaN with 0 (for days with no device activity)
    combined['device_connections'] = combined['device_connections'].fillna(0)
    
    # 4. Save final file
    combined.to_csv("data/processed/final_features.csv", index=False)
    print("Saved final_features.csv\n")
    print("=== Sample Output ===")
    print(combined.head())

if __name__ == "__main__":
    process_logons()
    process_devices()
    combine_features()
    print("\nALL DONE! Check the data/processed folder.")