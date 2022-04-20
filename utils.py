from geopy.geocoders import *
from meteostat import *
from urllib.request import urlopen
import subprocess as sp
import json
import time
import gettext
import requests
import re

geocoder = Nominatim(user_agent = 'utilslib')
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
    location = getPosFromCity(cityName)
    place = Point(location.latitude, location.longitude, 10)
    return place

def getIPdata():
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

def getStationIdWithCityName(cityName):
    stations = Stations()
    cityCoords = getPosFromCity(cityName) 
    stations = stations.nearby(cityCoords.latitude, cityCoords.longitude)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId

def getStationIdWithCoordinates(lat, long):
    stations = Stations() 
    stations = stations.nearby(lat, long)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId

def windowsGps():
    accuracy = 1000 #Starting desired accuracy is fine and builds at x1.5 per loop
    pshellcomm = ['powershell']
    pshellcomm.append('add-type -assemblyname system.device; '\
                        '$loc = new-object system.device.location.geocoordinatewatcher;'\
                        '$loc.start(); '\
                        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
                        '{start-sleep -milliseconds 100}; '\
                        '$acc = %d; '\
                        'while($loc.position.location.horizontalaccuracy -gt $acc) '\
                        '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
                        '$loc.position.location.latitude; '\
                        '$loc.position.location.longitude; '\
                        '$loc.position.location.horizontalaccuracy; '\
                        '$loc.stop()' %(accuracy))
    p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split('\n', out)

    out[0] = float(out[0].replace(",","."))
    out[1] = float(out[1].replace(",","."))
    location = geolocator.reverse((out[0], out[1]))
    address = location.raw['address']
    return address.get('city', '')

def getWttr(QUERY):
    urlWttr = 'https://wttr.in'
    res = requests.get(urlWttr + QUERY)
    return res.text