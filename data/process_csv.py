import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
import os

def load_and_process_csv(csv_file='data/nginx_logs.csv'):
    """
    Load the parsed CSV file and perform feature engineering
    """
    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found. Please run parse_logs.py first.")
        return None
    
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")
    
    # Feature engineering
    df = engineer_features(df)
    
    # Encode categorical features
    df_encoded, encoder_mappings = encode_features(df)
    
    # Save encoder mappings
    save_encoder_mappings(encoder_mappings, 'data/encoder_mappings.json')
    
    return df_encoded, encoder_mappings

def engineer_features(df):
    """
    Perform feature engineering on the dataframe
    """
    # Convert timestamp to datetime if it's not already
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract time-based features
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_night'] = ((df['hour_of_day'] >= 22) | (df['hour_of_day'] <= 6)).astype(int)
    
    # Path-based features
    if 'path' in df.columns:
        df['path_length'] = df['path'].str.len()
        df['has_query_params'] = df['path'].str.contains(r'\?').astype(int)
        df['path_depth'] = df['path'].str.count('/')
        
        # Suspicious path patterns
        df['suspicious_path'] = (
            df['path'].str.contains(r'\.\./', case=False, na=False) |
            df['path'].str.contains(r'etc/passwd', case=False, na=False) |
            df['path'].str.contains(r'admin', case=False, na=False) |
            df['path'].str.contains(r'config', case=False, na=False) |
            df['path'].str.contains(r'\.php', case=False, na=False)
        ).astype(int)
    
    # User agent features
    if 'user_agent' in df.columns:
        df['user_agent_length'] = df['user_agent'].str.len()
        df['is_bot'] = (
            df['user_agent'].str.contains(r'bot|crawler|spider|scraper', case=False, na=False)
        ).astype(int)
        df['is_mobile'] = (
            df['user_agent'].str.contains(r'Mobile|Android|iPhone', case=False, na=False)
        ).astype(int)
    
    # Status code categories
    if 'status' in df.columns:
        df['status_category'] = df['status'].apply(categorize_status)
        df['is_error'] = (df['status'] >= 400).astype(int)
        df['is_redirect'] = ((df['status'] >= 300) & (df['status'] < 400)).astype(int)
    
    # Size-based features
    if 'size' in df.columns:
        df['is_large_response'] = (df['size'] > 10000).astype(int)
        df['size_category'] = pd.cut(df['size'], 
                                   bins=[0, 100, 1000, 10000, float('inf')], 
                                   labels=['small', 'medium', 'large', 'huge'])
    
    # IP-based features (simplified)
    if 'ip' in df.columns:
        df['is_private_ip'] = df['ip'].apply(is_private_ip)
    
    return df

def categorize_status(status):
    """Categorize HTTP status codes"""
    if 200 <= status < 300:
        return 'success'
    elif 300 <= status < 400:
        return 'redirect'
    elif 400 <= status < 500:
        return 'client_error'
    elif 500 <= status < 600:
        return 'server_error'
    else:
        return 'other'

def is_private_ip(ip):
    """Check if IP is in private range (simplified)"""
    if ip.startswith(('192.168.', '10.', '172.')):
        return 1
    return 0

def encode_features(df):
    """
    Encode categorical features using LabelEncoder
    """
    # Features to encode
    categorical_features = ['method', 'path', 'user_agent', 'status_category', 'size_category']
    
    # Initialize encoders
    encoders = {}
    encoder_mappings = {}
    
    df_encoded = df.copy()
    
    for feature in categorical_features:
        if feature in df.columns:
            # Handle missing values
            df_encoded[feature] = df_encoded[feature].fillna('unknown')
            
            # Create and fit encoder
            encoder = LabelEncoder()
            df_encoded[feature] = encoder.fit_transform(df_encoded[feature].astype(str))
            
            # Store encoder and mapping
            encoders[feature] = encoder
            encoder_mappings[feature] = {
                str(label): int(encoded) for encoded, label in enumerate(encoder.classes_)
            }
    
    # Select features for ML model
    feature_columns = [
        'status', 'size', 'method', 'path', 'user_agent', 'hour_of_day',
        'day_of_week', 'is_weekend', 'is_night', 'path_length', 'has_query_params',
        'path_depth', 'suspicious_path', 'user_agent_length', 'is_bot', 'is_mobile',
        'is_error', 'is_redirect', 'is_large_response', 'is_private_ip'
    ]
    
    # Keep only available features
    available_features = [col for col in feature_columns if col in df_encoded.columns]
    df_ml = df_encoded[available_features]
    
    return df_ml, encoder_mappings

def save_encoder_mappings(encoder_mappings, filename):
    """Save encoder mappings to JSON file"""
    with open(filename, 'w') as f:
        json.dump(encoder_mappings, f, indent=2)
    print(f"Encoder mappings saved to {filename}")

def load_encoder_mappings(filename='data/encoder_mappings.json'):
    """Load encoder mappings from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Encoder mappings file {filename} not found.")
        return {}

def encode_single_log(log_data, encoder_mappings):
    """
    Encode a single log entry using saved encoder mappings
    """
    encoded_log = log_data.copy()
    
    for feature, mapping in encoder_mappings.items():
        if feature in encoded_log:
            value = str(encoded_log[feature])
            # Use mapping if available, otherwise assign a new encoding
            if value in mapping:
                encoded_log[feature] = mapping[value]
            else:
                # For unseen values, assign the maximum encoding + 1
                encoded_log[feature] = max(mapping.values()) + 1 if mapping else 0
    
    return encoded_log

if __name__ == "__main__":
    df_processed, mappings = load_and_process_csv()
    if df_processed is not None:
        print("\nProcessed dataset info:")
        print(f"Shape: {df_processed.shape}")
        print(f"Columns: {list(df_processed.columns)}")
        print("\nFirst few rows:")
        print(df_processed.head())
        
        print("\nDataset statistics:")
        print(df_processed.describe()) 