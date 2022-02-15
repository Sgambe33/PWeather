from datetime import *
from tkinter import messagebox
import pygubu
import utils
from meteostat import *
from tkinter import *

LOCATIONQUERY = "/?format=%l"
TEMPERATUREQUERY = "/?format=%t"
HUMIDITYQUERY = "/?format=%h"
PRECIPITATIONQUERY = "/?format=%p"
WCONDITIONQUERY = "/?format=%c"
LOCAL_CITY_NAME = utils.getWttr(LOCATIONQUERY)
class Application:
    #Definizione contenuto labels e frames
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('mainwindow.ui')
        self.mainwindow = builder.get_object('frame1', master)

        localName = self.builder.get_object('localName')
        localTime = self.builder.get_object('localTimeLabel')
        weatherIcon = self.builder.get_object('weatherIconLabel')
        localTemperatureLabel = self.builder.get_object('localTemperatureLabel')
        localHumidityLabel = self.builder.get_object('localHumidityLabel')
        localPrecipitationLabel = self.builder.get_object('localPrecipitationLabel')
        
        localTemperatureLabel.config(text="Temperature: \n" + utils.getWttr(TEMPERATUREQUERY))
        localHumidityLabel.config(text="Humidity: \n" + utils.getWttr(HUMIDITYQUERY))
        localPrecipitationLabel.config(text="Precipitation: \n" + utils.getWttr(PRECIPITATIONQUERY))
        localName.config(text=LOCAL_CITY_NAME)
        weatherIcon.config(text=utils.getWttr(WCONDITIONQUERY))

        def time():
            date=datetime.now()
            format_date=f"{date:%a, %d %b %Y \n%H : %M : %S}" 
            localTime.config(text=format_date) 
            localTime.after(1000, time)

        builder.connect_callbacks(self)

        time()

    #Azioni pulsanti
    def lstWeekBtn(self):
        start = datetime.today() - timedelta(days=7)
        end = datetime.today() 
        data = Daily(utils.getStationIdWithCityName(LOCAL_CITY_NAME), start, end )
        data = data.fetch() 
        messagebox.showinfo(title="Ultima settimana", message=str(data))   
        
    def weatherForecastBtn(self):
        messagebox.showinfo(title="Previsioni meteo", message="Ecco le previsioni")
        
    def weatherRecordsBtn(self):
        messagebox.showinfo(title="Archivi dati", message="Ecco gli archivi dati")
        
    def optionsBtn(self):
        messagebox.showinfo(title="Impostazioni", message="Hai aperto le impostazioni")
        
root = Tk()
app = Application(root)
root.mainloop()
