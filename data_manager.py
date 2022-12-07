import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()
# Create a .env file in root directory for all API keys and tokens

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_HEADER = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

class DataManager:
    """ Use the Sheety API to get and modify data in Google Sheet"""

    def __init__(self):
        self.search_data = {}

    def get_sheety_data(self):
        """ Returns data from 'prices' sheet """
        response = requests.get(url=SHEETY_ENDPOINT, headers=SHEETY_HEADER)
        response.raise_for_status()
        self.data = response.json()
        return self.data["prices"]

    def update_sheety_data(self):
        """ Updates the Iata codes for cities in 'prices' sheet """
        for city in self.data["prices"]:
            new_params = {
                "price": {
                 "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_params, headers=SHEETY_HEADER)

