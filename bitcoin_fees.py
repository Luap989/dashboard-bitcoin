import requests
from datetime import datetime, timedelta
import schedule
import json
import time

def get_fee_history():
    try:
        response = requests.get("https://mempool.space/api/v1/fees/recommended")
        if response.status_code == 200:
            data = response.json()
            print("API Response Data:", data)  # Add this line to print the API response data
            # Calculate yesterday's date
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_str = yesterday.strftime("%Y-%m-%d")
            # Get yesterday's fee history
            fee_history = data[yesterday_str]
            return fee_history
        else:
            print("Error retrieving data. Error code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            print("Data successfully saved to", filename)
    except Exception as e:
        print("An error occurred while saving data to JSON file:", str(e))

def print_fee_history():
    fee_history = get_fee_history()
    if fee_history is not None:
        print("Yesterday's fee history in sats/vbytes:")
        print(fee_history)
        # Save data to a JSON file
        save_to_json(fee_history, "fee_history.json")
    else:
        print("Unable to retrieve yesterday's fees.")

# Schedule the execution of the print_fee_history() function every day at midnight
schedule.every().day.at("00:00").do(print_fee_history)

while True:
    schedule.run_pending()
    time.sleep(60)  # Wait for 60 seconds before checking the schedule again
