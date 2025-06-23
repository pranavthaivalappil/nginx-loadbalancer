import re
import pandas as pd
import os
from datetime import datetime

def parse_nginx_log_line(line):
    """
    Parse a single NGINX access log line and extract relevant fields
    
    Log format: IP - - [timestamp] "METHOD /path HTTP/1.1" status size "referer" "user_agent"
    """
    # NGINX log pattern
    pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d+) (\d+) "([^"]*)" "([^"]*)"'
    
    match = re.match(pattern, line.strip())
    if match:
        ip = match.group(1)
        timestamp = match.group(2)
        method = match.group(3)
        path = match.group(4)
        protocol = match.group(5)
        status = int(match.group(6))
        size = int(match.group(7)) if match.group(7) != '-' else 0
        referer = match.group(8)
        user_agent = match.group(9)
        
        # Parse timestamp
        try:
            dt = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
        except:
            dt = datetime.strptime(timestamp.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
        
        return {
            'ip': ip,
            'timestamp': dt,
            'method': method,
            'path': path,
            'protocol': protocol,
            'status': status,
            'size': size,
            'referer': referer,
            'user_agent': user_agent,
            'hour_of_day': dt.hour,
            'day_of_week': dt.weekday()
        }
    return None

def parse_nginx_logs(log_file_path='data/nginx.log', output_file='data/nginx_logs.csv'):
    """
    Parse NGINX log file and save as CSV
    """
    parsed_logs = []
    
    if not os.path.exists(log_file_path):
        print(f"Log file {log_file_path} not found. Creating sample data...")
        create_sample_nginx_logs(log_file_path)
    
    print(f"Parsing {log_file_path}...")
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line_num, line in enumerate(file, 1):
            if line.strip():
                parsed_line = parse_nginx_log_line(line)
                if parsed_line:
                    parsed_logs.append(parsed_line)
                else:
                    print(f"Failed to parse line {line_num}: {line.strip()}")
    
    if parsed_logs:
        df = pd.DataFrame(parsed_logs)
        df.to_csv(output_file, index=False)
        print(f"Parsed {len(parsed_logs)} log entries and saved to {output_file}")
        return df
    else:
        print("No valid log entries found!")
        return None

def create_sample_nginx_logs(log_file_path):
    """
    Create sample NGINX logs for testing purposes
    """
    sample_logs = [
        '192.168.1.100 - - [10/Jan/2024:14:25:30 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"',
        '192.168.1.101 - - [10/Jan/2024:14:26:15 +0000] "POST /api/login HTTP/1.1" 200 512 "https://example.com/login" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"',
        '10.0.0.50 - - [10/Jan/2024:14:27:01 +0000] "GET /admin/config HTTP/1.1" 403 256 "-" "curl/7.68.0"',
        '192.168.1.102 - - [10/Jan/2024:14:28:45 +0000] "GET /images/logo.png HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)"',
        '203.0.113.45 - - [10/Jan/2024:14:29:12 +0000] "GET /../../../etc/passwd HTTP/1.1" 404 128 "-" "Nikto/2.1.6"',
        '192.168.1.103 - - [10/Jan/2024:14:30:00 +0000] "GET /dashboard HTTP/1.1" 200 4096 "-" "Mozilla/5.0 (Linux; Android 10; SM-G975F)"',
        '198.51.100.25 - - [10/Jan/2024:14:31:33 +0000] "POST /upload.php HTTP/1.1" 500 0 "-" "python-requests/2.25.1"',
        '192.168.1.104 - - [10/Jan/2024:14:32:18 +0000] "GET /api/users HTTP/1.1" 200 8192 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0)"'
    ]
    
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as f:
        for log in sample_logs:
            f.write(log + '\n')
    
    print(f"Created sample NGINX logs at {log_file_path}")

if __name__ == "__main__":
    df = parse_nginx_logs()
    if df is not None:
        print("\nFirst few parsed entries:")
        print(df.head())
        print(f"\nDataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}") 