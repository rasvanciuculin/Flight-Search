import requests
from flight_data import FlightData
import os
from dotenv import load_dotenv

load_dotenv()
# Create a .env file in root directory for all API keys and tokens

TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
TEQUILA_ENDPOINT_SEARCH = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_ENDPOINT_QUERY = "https://api.tequila.kiwi.com/locations/query"

class FlightSearch:
    """ Use the Tequila Kiwi API to search for flights"""

    def get_city_code(self, city_name):
        """ Returns Iata code for city (airport)"""

        query = {"term": city_name, "location_types": "city"}
        headers = {
            "apikey": TEQUILA_API_KEY,
        }

        response = requests.get(url=TEQUILA_ENDPOINT_QUERY, params=query, headers=headers)
        response.raise_for_status()
        data = response.json()["locations"]
        city_code  = data[0]["code"]
        return city_code

    def flight_check(self, fly_from_city_code, fly_to_city_code, date_from, date_to):
        """ Takes as input departure city, destination city, desired time period
        Returns flight data - if flight is available"""

        tequila_params = {
            "fly_from": fly_from_city_code,
            "fly_to": fly_to_city_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "one_for_city": 1,
            "sort": "price",
            "flight_type": "round",
            "max_stopovers": 0,
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 4
        }
        header = {
            "apikey": TEQUILA_API_KEY
        }

        response = requests.get(url=TEQUILA_ENDPOINT_SEARCH, params=tequila_params, headers=header)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
        except IndexError:
            # If no direct flight available checks for flights with a stop-over
            tequila_params["max_stopovers"] = 2
            response = requests.get(url=TEQUILA_ENDPOINT_SEARCH, params=tequila_params, headers=header)
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
                flight_data = FlightData(
                    price=data["price"],
                    fly_to=data["flyTo"],
                    fly_from=data["flyFrom"],
                    city_to=data["cityTo"],
                    city_from=data["cityFrom"],
                    departure_date=data["route"][0]['local_departure'].split("T", 1)[0],
                    nr_nights=data['nightsInDest'],
                    stop_over=2,
                    via_city=data['route'][0]['cityTo']
                )
                print(f"{flight_data.city_to}:  EUR {flight_data.price} via {flight_data.via_city}")
                return flight_data
            except IndexError:
                # No flight available
                return None

        else:
            # Returns flight data for direct flight
             flight_data = FlightData(
                 price=data["price"],
                 fly_to=data["flyTo"],
                 fly_from=data["flyFrom"],
                 city_to=data["cityTo"],
                 city_from=data["cityFrom"],
                 departure_date=data["route"][0]['local_departure'].split("T", 1)[0],
                 nr_nights=data['nightsInDest'],
                 stop_over=0,
                 via_city=""
             )
             print(f"{flight_data.city_to}: EUR {flight_data.price}")
             return flight_data


