from datetime import *
from tkinter import messagebox

import pygubu
import utils
from meteostat import *
from tkinter import *

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

        localName.config(text=utils.geojsip())
        start = datetime.now() - timedelta(0,0,0,0,0,1)
        end = datetime.now() 
        data = Hourly(utils.getStationIdWithIp(utils.geojsip()), start, end )
        data = data.fetch() 
        print(data)
        localTemperatureLabel.config(text="Temperature: \n" + str(data["temp"][0])+ "°C")
        localHumidityLabel.config(text="Temperature: \n" + str(data["rhum"][0]) + "%")
        localPrecipitationLabel.config(text="Precipitation: \n" + str(data["prcp"][0]) + "ml")

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
        data = Daily(utils.getStationIdWithIp(utils.geojsip()), start, end )
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
