import utils
from meteostat import *
from geopy.geocoders import *
from datetime import *
import gettext


en = gettext.translation('en', localedir='locales', languages=['en'])
it = gettext.translation('it', localedir='locales', languages=['it'])
en.install()
it.install()
_ = it.gettext

geolocator = Nominatim(user_agent="testgeopy")



while True:
    print(_("1. Mostra il meteo dell'ultima settimana."))
    print(_("2. Mostra il meteo di oggi."))
    print(_("3. Mostra le previsioni meteo. (WIP)"))
    print(_("4. Mostra i registri meteo."))
    print(_("5. Esci"))
    
    scelta = input()
    ipData = utils.getLocationFromIP()
    match scelta:
        case "1":
            start = datetime.today() - timedelta(days=7)
            end = datetime.today() 
            data = Daily(utils.getStationIdWithIp(ipData), start, end )
            data = data.fetch() 
            print(data) 
        case "2":
            start = datetime.now() - timedelta(hours=24)
            end = datetime.now()
            data = Hourly(utils.getStationIdWithIp(ipData), start, end )
            data = data.fetch() 
        case "3":
            print(_("Funzionalità in corso di sviluppo. Non disponibile."))
        case "4":
            #Inserimento delle date di inizio e fine registri
            print(_("Data di inizio dei registri:"))
            dataS = input(_('Enter a START date in YYYY-MM-DD format'))
            anno, mese, giorno = map(int, dataS.split('-'))
            start = datetime(anno, mese, giorno)
            #-------------------------------------------------------#
            dataE = input(_('Enter an END date in YYYY-MM-DD format'))
            anno, mese, giorno = map(int, dataE.split('-'))
            end = datetime(anno, mese, giorno)
            #-------------------------------------------------------#
            #Chiedo all'utente di inserire la loc. desiderata. Se non è trovata stampo errore e richiedo.
            while True:
                try:
                    print(_("Località: "))
                    cityName = input()
                    stations = Stations()
                    city = utils.getPosFromCity(cityName) 
                    stations = stations.nearby(city.latitude, city.longitude)
                    break
                except:
                    print(_("Località non trovata.Riprova"))
                    
            station = stations.fetch(1)
            stationId = station.filter(['id'])
            
            data = Daily(stationId, start, end)
            data = data.fetch() 
            print(data)
            
            #Chiedo il tipo di formato in cui salvare il file
            print(_("In che formato salvare i dati?"))
            print("1. HTML")
            print("2. CSV")
            print("3. JSON")
            print(_("4. Esci"))
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
                    print(_("Opzione non valida!"))  
        case "4":
            exit()
        case _:
            print(_("Opzione non valida!"))