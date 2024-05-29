import requests
from datetime import datetime, timedelta
import json

def get_historical_prices_between_dates(symbol, interval, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    interval_days = timedelta(days=500)  # Diviser la plage de dates en périodes de 500 jours maximum
    current_date = start_date
    daily_avg_prices = {}

    while current_date <= end_date:
        next_date = min(current_date + interval_days, end_date)
        start_timestamp = int(current_date.timestamp()) * 1000
        end_timestamp = int(next_date.timestamp()) * 1000

        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_timestamp,
            "endTime": end_timestamp
        }

        response = requests.get(url, params=params)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            for candlestick in data:
                timestamp = int(candlestick[0]) // 1000
                date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
                open_price = float(candlestick[1])
                close_price = float(candlestick[4])
                daily_avg_price = (open_price + close_price) / 2
                daily_avg_prices[date] = daily_avg_price

        current_date = next_date + timedelta(days=1)  # Déplacer la date de départ à la prochaine période

    return daily_avg_prices

# Exemple d'utilisation
symbol = 'BTCUSDT'  # Exemple pour BTC en USDT
interval = '1d'  # Interval de temps (1d = 1 jour)
start_date = '2017-08-17'  # Date de début au format 'YYYY-MM-DD' min est : 2017-08-17
end_date = '2024-05-17'  # Date de fin au format 'YYYY-MM-DD'

historical_prices = get_historical_prices_between_dates(symbol, interval, start_date, end_date)

if historical_prices:
    # Stocker les données historiques réelles dans le dictionnaire 'data'
    data = {
        symbol: historical_prices
    }

    # Chemin vers le fichier JSON de sortie
    output_file = "historical_prices.json"

    # Écrire les données dans le fichier JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Données stockées avec succès dans", output_file)
else:
    print("Aucune donnée historique disponible.")


