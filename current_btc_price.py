import requests
import json
from datetime import datetime

def get_current_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'bitcoin' in data.keys() and 'usd' in data['bitcoin'].keys():
            return data['bitcoin']['usd']
    return None

def main():
    current_price = get_current_bitcoin_price()
    if current_price:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {'timestamp': timestamp, 'price_usd': current_price}
        with open('bitcoin_current_price.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("La valeur actuelle du Bitcoin a été enregistrée dans le fichier bitcoin_current_price.json.")
    else:
        print("Impossible de récupérer la valeur actuelle du Bitcoin.")

if __name__ == "__main__":
    main()
