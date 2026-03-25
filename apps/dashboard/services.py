import pandas as pd
import os

def load_crime_data():
    file_path = os.path.join('data', 'crime_data.csv')
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return None