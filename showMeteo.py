# Import Meteostat library and dependencies
from logging import exception
from meteostat import *
from geopy.geocoders import *
from datetime import *
from prettytable import PrettyTable
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt

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

def getStationIdWithIp(ipdata):
    stations = Stations()
    city = getPosFromCity(ipdata['city']) 
    stations = stations.nearby(city.latitude, city.longitude)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId
    
start= datetime(2022, 1, 1)
end = datetime.today()

data = Daily('16124', start, end )
data = data.fetch() 
print(data)

while True:
    print("1. Mostra il meteo dell'ultima settimana.")
    print("2. Mostra il meteo di oggi.")
    print("3. Mostra le previsioni meteo. (WIP)")
    print("4. Mostra i registri meteo.")
    print("4. Esci")
    
    scelta = input()
    
    match scelta:
        case "1":
            start = datetime.today() - timedelta(days=7)
            end = datetime.today()
            ipData = getLocationFromIP()          
            data = Daily(getStationIdWithIp(ipData), start, end )
            data = data.fetch() 
            print(data) 
        case "2":
            print("null")
        case "3":
            print("null")
        case "4":
            print("null")
        case "5":
            exit()
    print("lOOP")








""" print("Dove sei??")
try:
    gps = getLocationFromIP()
    print(gps['city'], gps['region'], gps['country'])
except:
    print("Impossibile ottenere la tua posizione!") """








