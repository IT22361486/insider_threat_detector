import os
import pandas as pd

def explore_dataset():
    data_path = "data/raw/r1"
    csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    print(f"Found {len(csv_files)} CSV files in {data_path}:")
    for file in csv_files:
        print(f"- {file}")
    
    for file in csv_files:
        print(f"\n=== Exploring {file} ===")
        try:
            # Read first few rows to detect headers
            df = pd.read_csv(os.path.join(data_path, file), nrows=5)
            
            # If first column looks like an ID, use first row as header
            if df.columns[0].startswith('{'):
                df = pd.read_csv(os.path.join(data_path, file), header=0)
            else:
                df = pd.read_csv(os.path.join(data_path, file))
            
            print(f"\nShape: {df.shape} (rows, columns)")
            print("\nFirst 3 rows:")
            print(df.head(3))
            
            print("\nColumn names:")
            print(list(df.columns))
            
            print("\nMissing values per column:")
            print(df.isnull().sum())
            
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")

if __name__ == "__main__":
    explore_dataset()