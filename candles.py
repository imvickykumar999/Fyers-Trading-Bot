# Install necessary libraries if not already installed
# !pip install matplotlib pandas fyers-apiv2

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import time
from datetime import datetime, timedelta
from fyers_api import fyersModel
from matplotlib.animation import FuncAnimation
from pprint import pprint as p

# Replace with your actual client ID and access token
client_id = "2A6LCH4LF8-100"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MTk0NjQ2NDAsImV4cCI6MTcxOTUzNDYwMCwibmJmIjoxNzE5NDY0NjQwLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbWZQTEE3b2pkd19nT0NrR1diQUxKRXBxcmRaOFhWN3dSNW55Z0ZaOWNPa21ZMWZIYVZmaDZmVmpfRnAxNXY2ZXU2dFh0SmRPUTQxS1FlbjBPUENFeDdwQXlYZFMxM3VrbFNHWWU2dFQxQVBLMDNOUT0iLCJkaXNwbGF5X25hbWUiOiJQUklZQU5LQSBHVVBUQSIsIm9tcyI6IksxIiwiaHNtX2tleSI6IjdhYjY3OTI0NzQ5MDY0Y2E0MmEzOWExNmU0MmIxOTJmY2Q0NTlkZDhlNWU5MDZhMmQ5NzVkNTk4IiwiZnlfaWQiOiJZUDExMjYzIiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.znxz_lLkv6QOCe2M2VpEnVTPdnYIgRheTculur_Kpac"  # Make sure to replace with your actual access token

log_path = os.path.join(os.getcwd(), "fyers_logs")

# Create the directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path=log_path)

# Define the date range for the last one year
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Convert the date range to Unix timestamps
range_from = int(start_date.timestamp())
range_to = int(end_date.timestamp())

# Define the data for the API request
data = {
    "symbol": "BSE:FRASER-X",
    "resolution": "D",
    "date_format": "0",
    "range_from": str(range_from),
    "range_to": str(range_to),
    "cont_flag": "1"
}

# Initialize the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
counter = 0

# Function to fetch data and update the plot
def update(frame):
    global range_to, counter
    range_to = int(datetime.now().timestamp())
    data["range_to"] = str(range_to)
    
    response = fyers.history(data=data)
    counter += 1
    p(response)
    print(counter)
    
    if response['s'] == 'ok':
        candles = response['candles']
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(candles, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        ax1.clear()
        ax2.clear()
        
        for index, row in df.iterrows():
            color = 'green' if row['close'] >= row['open'] else 'red'
            ax1.plot([row['timestamp'], row['timestamp']], [row['low'], row['high']], color='black')
            ax1.plot([row['timestamp'], row['timestamp']], [row['open'], row['close']], color=color, linewidth=5)
        
        ax2.bar(df['timestamp'], df['volume'], color='blue', alpha=0.6)
        
        ax1.set_title(f'Candlestick Chart for [ {data["symbol"]} ]\n')
        ax1.set_ylabel('Price')
        ax2.set_ylabel('Volume')
        
        ax1.grid(True)
        ax2.grid(True)
        plt.xticks(rotation=30)
    else:
        print("Failed to fetch data:", response)

# Create an animation
ani = FuncAnimation(fig, update, interval=9000, cache_frame_data=False)  # Update every 9 seconds

plt.show()

