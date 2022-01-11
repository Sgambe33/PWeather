# Import Meteostat library and dependencies
from logging import exception
import math
from fpdf import *
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
    while True:
        try:
            response = urlopen(url)
            ipInfo = json.load(response)
        except:
            print("Errore di connessione...")
            print("Ritento...")
        finally:
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
            print("Data di inizio dei registri:")
            dataS = input('Enter a date in YYYY-MM-DD format')
            anno, mese, giorno = map(int, dataS.split('-'))
            start = datetime.date(anno, mese, giorno)
            #####################################################
            dataE = input('Enter a date in YYYY-MM-DD format')
            anno, mese, giorno = map(int, dataE.split('-'))
            end = datetime.date(anno, mese, giorno)
            #####################################################
            print("Posizione: ")
            cityName = input()
            stations = Stations()
            city = getPosFromCity(cityName) 
            stations = stations.nearby(city.latitude, city.longitude)
            station = stations.fetch(1)
            stationId = station.filter(['id'])
            
            data = Monthly(stationId, start, end)
            
            data = data.fetch() 
            print("In che formato salvare i dati?")
            print("1. HTML")
            print("2. PDF")
            print("3. CSV")
            print("4. JSON")
            fileType = input()
            match fileType:
                case "1":
                    data.to_html("records.html")
                case "2":
                    pdf = FPDF()  
                    pdf.add_page()
                    pdf.set_font("Arial", size = 15)
                    f = open("myfile.txt", "r")
                    pdf.cell(200, 10, txt = data, ln = 1, align = 'C')
                    pdf.output("records.pdf")   
                case "3":
                    data.to_csv("records.csv")
                case "4":
                    data.to_json("records.json")
                
        case "5":
            exit()
        case _:
            print("Opzione non valida!")








""" print("Dove sei??")
try:
    gps = getLocationFromIP()
    print(gps['city'], gps['region'], gps['country'])
except:
    print("Impossibile ottenere la tua posizione!") """








