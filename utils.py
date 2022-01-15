from geopy.geocoders import *
from meteostat import *
from urllib.request import urlopen
import json
import time
import gettext
#Localization part
en = gettext.translation('en', localedir='locales', languages=['en'])
it = gettext.translation('it', localedir='locales', languages=['it'])
en.install()
it.install()
_ = it.gettext
#Function declaration part
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
            
def getStationIdWithIp(ipdata):
    stations = Stations()
    city = getPosFromCity(ipdata['city']) 
    stations = stations.nearby(city.latitude, city.longitude)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId