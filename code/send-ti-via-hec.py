import requests
import json
import os

# Constants
API_URL = "https://api.intel471.com/data"
HEC_URL = "https://ingest.us1.sentinelone.net/services/collector/event"
HEC_TOKEN = "your_hec_token_here"

# Function to query the API
def query_api():
    # Example query to the API
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()  # Assuming JSON response
    else:
        return None

# Function to send data to SentinelOne HEC
def send_to_hec(batch_data):
    headers = {
        "Authorization": f"Bearer {HEC_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(HEC_URL, headers=headers, json=batch_data)
        response.raise_for_status()
        print("Data sent successfully to SentinelOne HEC.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to SentinelOne HEC: {e}")

# Main function to accumulate and send data
def main():
    batch_size_limit = 5 * 1024 * 1024  # 5MB limit in bytes
    accumulated_data = []
    total_size = 0

    while total_size < batch_size_limit:
        data = query_api()
        if not data:
            break
        
        # Accumulate data
        accumulated_data.append({
            "host": "your_host",  #maps to serverHost in s1
            "source": "your_source", #maps to serverHost in s1
            "sourcetype": "intel471",#maps to serverHost in s1
            "index": "your_index", #not needed but you can use it
            "event": data #this is the object containing your code
        })
        
        total_size += len(json.dumps(data))  # Calculate JSON size in bytes

    if accumulated_data:
        send_to_hec(accumulated_data)
    else:
        print("No data accumulated or error during API queries.")

if __name__ == "__main__":
    main()
