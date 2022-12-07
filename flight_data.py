class FlightData:
    """ Returns flight data"""

    def __init__(self, price, fly_to, fly_from, city_to, city_from, departure_date, nr_nights, stop_over=0, via_city=""):
        self.price = price
        self.fly_to = fly_to
        self.fly_from = fly_from
        self.city_from = city_from
        self.city_to = city_to
        self.departure_date = departure_date
        self.nr_nights = nr_nights
        self.stop_over = stop_over
        self.via_city = via_city