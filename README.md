># `Fyers-Trading-Bot`
>
>![image](https://github.com/imvickykumar999/Fyers-Trading-Bot/assets/50515418/6130520f-fe00-4850-bf4f-bd94ab8b3970)
>![candles](https://github.com/imvickykumar999/Fyers-Trading-Bot/assets/50515418/7a2765c1-602c-4f9a-979b-30d619e1a61b)

<br>

    To avoid hitting the rate limits while updating the plot 
    as frequently as possible, we need to find a balance. 

Given the rate limits:
---

- **Per Second**: 10 requests
- **Per Minute**: 200 requests
- **Per Day**: 10,000 requests


### Calculation:
1. **Per Second**: The maximum is 10 requests per second. If we set `interval=1000` (1 second), we would be making 1 request per second, which is safe.
2. **Per Minute**: The maximum is 200 requests per minute. If we set `interval=1000` (1 second), this would result in 60 requests per minute, which is well within the limit.
3. **Per Day**: The maximum is 10,000 requests per day. If we set `interval=1000` (1 second), this would result in 60 * 60 * 24 = 86,400 requests per day, which exceeds the limit.

<br>

To avoid exceeding the daily limit, we need to adjust the interval to a value that keeps us within the daily limit.

![image](https://github.com/imvickykumar999/Fyers-Trading-Bot/assets/50515418/2be3f9c4-39c2-4341-9a4d-8031df1132ac)

### Updated Code:
Here’s the updated code with the interval set to 9000 milliseconds (9 seconds):

```python
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

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.********.znxz_lLkv6QOCe2M2VpEnVTPdnYIgRheTculur_Kpac"
log_path = os.path.join(os.getcwd(), "fyers_logs")

# Create the directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path=log_path)

# Define the date range for the last one year
end_date = datetime.now()
start_date = end_date - timedelta(days=364)

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
```

### Explanation:
1. **Interval**: Set to `9000` milliseconds (9 seconds) to stay within the daily request limit.
2. **API Call Frequency**: This will make approximately 9,600 requests per day, which is under the 10,000 request limit and respects the per second and per minute limits.
