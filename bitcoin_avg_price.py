import json
import requests
from datetime import datetime, timedelta

def get_yesterday_date():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_avg_bitcoin_price():
    yesterday_date = get_yesterday_date()
    start_timestamp = int(datetime.strptime(yesterday_date, '%Y-%m-%d').timestamp()) * 1000
    end_timestamp = start_timestamp + 86400000  # Ajouter une journée en millisecondes

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",    # BTC/USDT pour le prix du Bitcoin en dollars US
        "interval": "1d",       # Données journalières
        "startTime": start_timestamp,
        "endTime": end_timestamp
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            # Calculer la moyenne des prix d'ouverture et de clôture de chaque bougie
            avg_price = sum((float(candlestick[1]) + float(candlestick[4])) / 2 for candlestick in data) / len(data)
            return avg_price
    return None

def main():
    avg_price = get_avg_bitcoin_price()
    if avg_price:
        yesterday_date = get_yesterday_date()
        new_data = {yesterday_date: avg_price}

        # Chemin vers le fichier JSON existant
        json_file = "historical_prices.json"

        try:
            # Ouvrir le fichier JSON et charger les données existantes
            with open(json_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            # Si le fichier n'existe pas encore, créer un dictionnaire vide
            data = {}

        # Vérifier si le dictionnaire principal existe déjà dans les données
        if "historical_prices" in data:
            # Ajouter les nouvelles données au dictionnaire principal existant
            data["historical_prices"].update(new_data)
        else:
            # Créer un nouveau dictionnaire principal et y ajouter les nouvelles données
            data["historical_prices"] = new_data

        # Écrire les données mises à jour dans le fichier JSON
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Le prix moyen du Bitcoin le {yesterday_date} était de ${avg_price}. Données ajoutées avec succès dans {json_file}")
    else:
        print("Impossible de récupérer le prix moyen du Bitcoin pour hier.")

if __name__ == "__main__":
    main()
