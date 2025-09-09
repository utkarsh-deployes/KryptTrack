import requests
from flask import Flask, render_template
import os
import time

app = Flask(__name__)

# Simple in-memory cache
cache = {
    'data': None,
    'timestamp': 0,
    'cache_duration': 60  # Cache for 60 seconds
}

def get_crypto_prices():
    """Fetches crypto prices from the CoinGecko API with caching."""
    
    current_time = time.time()
    
    # Return cached data if it's still fresh
    if (cache['data'] is not None and 
        current_time - cache['timestamp'] < cache['cache_duration']):
        print("Returning cached data...")
        return cache['data']
    
    coins = "bitcoin,ethereum,dogecoin,cardano,solana"
    currencies = "usd,inr"
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies={currencies}"
    
    try:
        print("Fetching live crypto prices...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("Successfully fetched data.")
        
        # Update cache
        cache['data'] = data
        cache['timestamp'] = current_time
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"Could not fetch data from API: {e}")
        
        # Return cached data if available, even if expired
        if cache['data'] is not None:
            print("Returning stale cached data due to API error...")
            return cache['data']
        
        # Return sample data if no cache available
        return {
            "bitcoin": {"usd": 0, "inr": 0},
            "ethereum": {"usd": 0, "inr": 0},
            "dogecoin": {"usd": 0, "inr": 0},
            "cardano": {"usd": 0, "inr": 0},
            "solana": {"usd": 0, "inr": 0}
        }

@app.route('/')
def index():
    crypto_data = get_crypto_prices()
    return render_template('index.html', data=crypto_data)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "KryptTracker"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)