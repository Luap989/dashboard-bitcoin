import requests

def get_transaction_fees():
    url = 'https://bitcoiner.live/api/fees/estimates/latest'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    fees_data = get_transaction_fees()
    if fees_data and 'estimates' in fees_data:
        print("Historique des frais de transaction du Bitcoin :")
        print("------------------------------------------------------")
        print(f"{'Fee Level':<15}{'Fee (Satoshis/Byte)':<25}")
        print("------------------------------------------------------")
        for fee_level, fee_info in fees_data['estimates'].items():
            fee_rate = fee_info['total']['p2pkh']['satoshi']
            print(f"{fee_level:<15}{fee_rate:<25}")
    else:
        print("Impossible de récupérer les données des frais de transaction ou les données reçues sont vides.")

if __name__ == "__main__":
    main()
