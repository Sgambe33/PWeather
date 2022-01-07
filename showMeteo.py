# Import Meteostat library and dependencies
from logging import exception
from meteostat import *
from geopy.geocoders import *
from datetime import *
from prettytable import PrettyTable
import re
import json
from urllib.request import urlopen

geolocator = Nominatim(user_agent="testgeopy")

def getPosFromCity(cityName):
    location=geolocator.geocode(cityName)
    return location

def getPlaceFromCity(cityName):
    location = getPosFromCity(cityName=cityName)
    place = Point(location.latitude, location.longitude, 10)
    return place

def getLocationFromIP():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    ipInfo = json.load(response)
    return ipInfo

start= datetime(2022, 1, 1)
end = datetime(2022, 1, 7)

data = Daily('16124', start, end )
data = data.fetch() 
print(type(data))

x = PrettyTable()

x.field_names = data.columns

for i in range(0,7, 1):
    x.add_row(data.iloc[i])



print(x)













""" print("Dove sei??")
try:
    gps = getLocationFromIP()
    print(gps['city'], gps['region'], gps['country'])
except:
    print("Impossibile ottenere la tua posizione!") """

