import requests
from flask import Flask, render_template

app = Flask(__name__)

def get_crypto_prices():
    """Fetches crypto prices from the CoinGecko API."""
    
    coins = "bitcoin,ethereum,dogecoin,cardano,solana"
    currencies = "usd,inr"
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies={currencies}"
    
    try:
        print("Fetching live crypto prices...")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        print("Successfully fetched data.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Could not fetch data from API: {e}")
        return None

@app.route('/')
def index():
    crypto_data = get_crypto_prices()
    return render_template('index.html', data=crypto_data)

if __name__ == '__main__':
    app.run(debug=True)