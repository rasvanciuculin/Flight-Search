# Flight search takes input from a Google Sheet
# with cities to travel to and a flight price desired for each city

# Check for the cheapest flights from tomorrow to 6 months later
# for all the cities in the Google Sheet

# If the price is lower than the lowest price listed in the Google Sheet
# send SMS to telephone number

from datetime import date
from dateutil.relativedelta import relativedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_IATA_CODE= "BUH"
# Iata code for Bucharest - can be changed for other cities (airports)

today = date.today()
tommorow = today + relativedelta(days=+ 1)
after_six_month = today + relativedelta(months=+ 6)

data_manager = DataManager()
flight_search = FlightSearch()

my_destinations_sheet = data_manager.get_sheety_data()

for row in my_destinations_sheet:
    # Populate the Google Sheet with Iata codes for every city (airport) in Google Sheet
    if row["iataCode"] == "":
        city_code = flight_search.get_city_code(row["city"])
        row["iataCode"] = city_code
        data_manager.search_data = my_destinations_sheet
        data_manager.update_sheety_data()

    city_code = flight_search.get_city_code(row["city"])
    # Check if there are flights to every city in Google Sheet
    flight = flight_search.flight_check(DEPARTURE_CITY_IATA_CODE, city_code, date_from=tommorow, date_to=after_six_month)
    if flight is None:
        print(f"No flight found to {row['city']}")
    elif flight.price <= row['lowestPrice']:
        # Send SMS if the flight price is lower than the price in Google Sheet
        notification = NotificationManager()
        notification.send_SMS(flight.price,
                              flight.city_to,
                              flight.fly_to,
                              flight.city_from,
                              flight.fly_from,
                              flight.departure_date,
                              flight.nr_nights)


