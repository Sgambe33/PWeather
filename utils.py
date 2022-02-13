from geopy.geocoders import *
from meteostat import *
from urllib.request import urlopen
import json
import time
import gettext
import requests
#Localization part
en = gettext.translation('en', localedir='locales', languages=['en'])
it = gettext.translation('it', localedir='locales', languages=['it'])
en.install()
it.install()
_ = it.gettext
#Function declaration part
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
    while True:
        try:
            response = urlopen(url)
            ipInfo = json.load(response)
            return ipInfo
        except:
            print(_("Errore di connessione..."))
            print(_("Ritento tra 15s..."))
            time.sleep(15)
    
def geojsip():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    return(geo_data["city"])

def getStationIdWithIp(cityName):
    stations = Stations()
    cityCoords = getPosFromCity(cityName) 
    stations = stations.nearby(cityCoords.latitude, cityCoords.longitude)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId