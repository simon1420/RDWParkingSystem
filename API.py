import os
import requests
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import csv
import PSdebug
import config
from car import Car

# TODO: PRETTY UP THE ENTIRE FILE
# TODO: Can be made more global but for testing purposes static has been chosen.
class RDWAPI:
    # Overview
    # TODO: Function that gets record based on URL i.e def get_data_by_query(query)
    """
    Init creates an object based on the API data, the get car function only neeeds an number plate and will return a car object
    """

    # Setting up the basic configuration for APIs, for the scope of this project (as of 6th of November 2017) the only planned API found at https://overheid.io/documentatie/voertuiggegevens
    def __init__(self):
        # TODO: Needs to be more dynamic to be able to use different types of login credentials i.e OAuth
        # Using authentication from OS rather than key to prevent collisions and license revokes due to public publication
        # self.auth = {'app_token': os.environ['OPEN_DATA-KEY'], 'hash': os.environ['OPEN_DATA-HASH']}

        # TODO: Dynamically allow endpoints i.e vehicle, brand etc
        self.url = 'https://opendata.rdw.nl/resource/m9d7-ebf2.json'
        self.separator = '?'
        self.number_plate_query_var = 'kenteken='

    """
    Currently there isn't one dataset with all the information we want which is 
        1.The first time it was assigned in the netherlands
        2.The fuel type i.e Gas, Diesel, Electric etc
    """

    # TODO: Function that gets data based on the inserted datatype and protocol set i.e number plate
    def get_car(self, number_plate):
        if number_plate is None:
            raise ValueError('Number plate is unknown /= None')
        query = number_plate

        APIquery = self.separator + self.number_plate_query_var + query

        # finally sending out to the overheid.io API access point
        response = requests.get(self.url + APIquery)

        # TODO: RESPONSE NEEDS TO BE CLEANSED
        car_data = json.loads(response.text)[0]

        # second api call to get the fuel type
        fuelType = requests.get(car_data['api_gekentekende_voertuigen_brandstof'] + APIquery).text

        fuel = json.loads(fuelType)[0]

        car_data.update(fuel)
        # TODO: WAAY more fail safes and exceptions placed
        return Car(**car_data)



