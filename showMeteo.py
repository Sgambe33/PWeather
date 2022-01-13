# Import Meteostat library and dependencies
from __future__ import barry_as_FLUFL
import os
from meteostat import *
from geopy.geocoders import *
from datetime import *
import time
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
    while True:
        try:
            response = urlopen(url)
            ipInfo = json.load(response)
            return ipInfo
        except:
            print("Errore di connessione...")
            print("Ritento tra 15s...")
            time.sleep(15)
            

def getStationIdWithIp(ipdata):
    stations = Stations()
    city = getPosFromCity(ipdata['city']) 
    stations = stations.nearby(city.latitude, city.longitude)
    station = stations.fetch(1)
    stationId = station.filter(['id'])
    return stationId

while True:
    print("1. Mostra il meteo dell'ultima settimana.")
    print("2. Mostra il meteo di oggi.")
    print("3. Mostra le previsioni meteo. (WIP)")
    print("4. Mostra i registri meteo.")
    print("5. Esci")
    
    scelta = input()
    ipData = getLocationFromIP()
    match scelta:
        case "1":
            start = datetime.today() - timedelta(days=7)
            end = datetime.today() 
            data = Daily(getStationIdWithIp(ipData), start, end )
            data = data.fetch() 
            print(data) 
        case "2":
            start = datetime.now() - timedelta(hours=24)
            end = datetime.now()
            data = Hourly(getStationIdWithIp(ipData), start, end )
            data = data.fetch() 
        case "3":
            print("Funzionalità in corso di sviluppo. Non disponibile.")
        case "4":
            #Inserimento delle date di inizio e fine registri
            print("Data di inizio dei registri:")
            dataS = input('Enter a START date in YYYY-MM-DD format')
            anno, mese, giorno = map(int, dataS.split('-'))
            start = datetime(anno, mese, giorno)
            #-------------------------------------------------------#
            dataE = input('Enter an END date in YYYY-MM-DD format')
            anno, mese, giorno = map(int, dataE.split('-'))
            end = datetime(anno, mese, giorno)
            #-------------------------------------------------------#
            #Chiedo all'utente di inserire la loc. desiderata. Se non è trovata stampo errore e richiedo.
            while True:
                try:
                    print("Località: ")
                    cityName = input()
                    stations = Stations()
                    city = getPosFromCity(cityName) 
                    stations = stations.nearby(city.latitude, city.longitude)
                    break
                except:
                    print("Località non trovata.Riprova")
                    
            
            station = stations.fetch(1)
            stationId = station.filter(['id'])
            
            data = Daily(stationId, start, end)
            data = data.fetch() 
            print(data)
            #Chiedo il tipo di formato in cui salvare il file
            print("In che formato salvare i dati?")
            print("1. HTML")
            print("2. CSV")
            print("3. JSON")
            print("4. Esci")
            fileType = input()
            
            match fileType:
                case "1":
                    data.to_html("records.html")
                case "2":
                    data.to_csv("records.csv")
                case "3":
                    data.to_json("records.json")    
                case "4":
                    break
                case _:
                    print("Opzione non valida!")  
        case "4":
            exit()
        case _:
            print("Opzione non valida!")










