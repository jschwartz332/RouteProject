"""
Program: Coldest Trip
Author: Jacob Schwartz
Last Date Modified: 5/8/2019
Purpose: Provides the lowest average temperature for your trip through a list of cities
"""

import requests
import json
from itertools import permutations

API_KEY = "7b828f09d62bb4d9426f388dff121afb"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"

class City:
    """Represents a city with a name and list of highest temperatures for 5 days"""
    def __init__(self, name, temperatures):
        """Declares and initializes the City class variables"""
        self.name = name
        self.temperatures = temperatures

    def get_temperature(self, day):
        """Returns the temperature of a day in a city"""
        return self.temperatures[day]

    def __str__(self):
        """Returns the name of the city object"""
        return self.name


class Route:
    """Represents a trip through cities"""
    def __init__(self, trip):
        """Declares and initializes the Route class variables"""
        #assuming trip is a list containing cities and max temps for each day
        self.trip = trip

    def avg_temps(self):
        """Calculates the average temperature of the trip through the cities"""
        average_temp = 0
        for j in range(len(self.trip)):
            average_temp += self.trip[j].get_temperature(j)
        average_temp /= len(self.trip)
        return average_temp


    def __str__(self):
        """Returns Route object"""
        return self.trip


def fetch_weather(y):
    """Receives name and max temperatures of each city and creates City objects"""
    # request parameter(s): Start with '?'
    # separate name and value with '='
    # multiple parameter name value pairs are separate with '&'
    query_string = "?id={}&units=imperial&APIKEY={}".format(y, API_KEY)
    request_url = WS_URL + query_string
    print("Request URL: ", request_url)
    response = requests.get(request_url)
    if response.status_code == 200:
        city_name = response.json()["city"]["name"]
        lst = response.json()["list"]
        tmp_list = []
        for i in range(len(lst) // 8):
            li = [x for x in range(len(lst)) if x // 8 == i]
            tmp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
        return City(city_name, tmp_list)
    else:
        print("How should I know?")
        return None

def route_creation():
    """Creates Route objects by sending name and list of max temperatures to Route class"""
    city_ids = json.loads(open("cities.json").read())
    cities = []
    for id in city_ids:
        cities.append(fetch_weather(id))
    return Route(cities)


if __name__ == "__main__":
    city_ids = json.loads(open("cities.json").read())
    cities = []
    for id in city_ids:
        cities.append(fetch_weather(id))
    avg_temp = 0
    newest_list = [] # Becomes list of city temperature permutations
    for i in range(len(cities)):
        city = cities[i]
        newest_list.append(city.temperatures)
        avg_temp += city.get_temperature(i)
    p = [list(j) for j in permutations(newest_list[i])]
    added_values = [] # Becomes list of values of city trip temperatures added together
    for o in p:
        added_values.append(sum(o))
    average_of_perm = [] # Becomes list of averages of all trip permutations
    for g in added_values:
        average_of_perm.append(g/5)
    print("The Lowest average temperature is: ", min(average_of_perm)) # Prints lowest average

"""
This is as far as I could get. I tried to input 'newest_list' into the permutations, but I couldn't
figure it out. I spent the total of my time trying to figure it out and ran out of time.
"""