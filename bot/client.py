#finance client 
#loading api credentials - initialise binance client - return client object

import os 
from dotenv import load_dotenv
from binance.client import Client

TESTNET_URL = "https://testnet.binancefuture.com"

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

def get_client():
    #create and return a binance futures client


    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET_KEY")

    if not api_key or not api_secret:
        raise ValueError(
            "API credentials not found. "
            "Please set BINANCE_API_KEY and BINANCE_SECRET_KEY in .env"
        )
    
    client = Client(api_key,api_secret)
    #redirect future request to testnet

    client.FUTURES_URL = f"{TESTNET_URL}/fapi"
    return client 

print("API:", api_key[:10])
print("SECRET:", api_secret[:10])
print(len(api_key))
print(len(api_secret))


    

