# src/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def add_threat_labels(df):
    """Add threat labels based on rules:
    0 = Normal (≤5 logins AND ≤2 devices)
    1 = Warning (>5 logins OR >2 devices)
    2 = Critical (>10 logins AND >5 devices)
    """
    df['threat_level'] = 0  # Default normal
    
    # Warning conditions
    df.loc[
        (df['logins_per_day'] > 5) | 
        (df['device_connections'] > 2), 
        'threat_level'
    ] = 1
    
    # Critical conditions
    df.loc[
        (df['logins_per_day'] > 10) & 
        (df['device_connections'] > 5), 
        'threat_level'
    ] = 2
    
    return df

def train_model():
    # 1. Load data
    data = pd.read_csv("data/processed/final_features.csv")
    
    # 2. Add labels
    labeled_data = add_threat_labels(data)
    
    # 3. Save labeled data (NEW)
    labeled_data.to_csv("data/processed/final_features_labeled.csv", index=False)
    
    # 4. Train model
    X = labeled_data[['logins_per_day', 'device_connections']]
    y = labeled_data['threat_level']
    
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # 5. Save model
    joblib.dump(model, "data/results/threat_model.pkl")
    print("Model trained and saved with threat labels!")

if __name__ == "__main__":
    train_model()