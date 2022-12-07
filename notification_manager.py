from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
# Create a .env file in root directory for all API keys and tokens

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
YOUR_NUMBER = os.environ.get("YOUR_NUMBER")

class NotificationManager:
    """ send SMS with flight info """

    def send_SMS(self, price, city_dest, airport_dest, city_departure, airport_departure, fly_date, nr_nights):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
            body=f"Low price alert! "
                 f"Fly from {city_departure}-{airport_departure} "
                 f"to {city_dest}-{airport_dest} "
                 f"starting from {fly_date} for {nr_nights} nights "
                 f"for EUR {price}",
            from_=TWILIO_NUMBER,
            to=YOUR_NUMBER
        )
        print(message.status)