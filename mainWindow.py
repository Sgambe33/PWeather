from datetime import *
import pathlib
from tkinter import messagebox
from turtle import width
import webbrowser
import pygubu
import utils
from meteostat import *
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

LOCATIONQUERY = "/?format=%l"
TEMPERATUREQUERY = "/?format=%t"
HUMIDITYQUERY = "/?format=%h"
PRECIPITATIONQUERY = "/?format=%p"
WCONDITIONQUERY = "/?format=%c"
LOCAL_CITY_NAME = utils.getWttr(LOCATIONQUERY)
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "mainwindow.ui"

start = datetime.today() - timedelta(hours=24)
end = datetime.today() 
data = Hourly(utils.getStationIdWithCityName(LOCAL_CITY_NAME), start, end )
data = data.fetch() 
print(str(data["temp"]))
class Application:
    #Definizione contenuto labels e frames
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('frame1', master)

        localName = self.builder.get_object('localName')
        localTime = self.builder.get_object('localTimeLabel')
        weatherIcon = self.builder.get_object('weatherIconLabel')
        localTemperatureBtn = self.builder.get_object('localTemperatureBtn')
        localHumidityBtn = self.builder.get_object('localHumidityBtn')
        localPrecipitationBtn = self.builder.get_object('localPrecipitationBtn')
        plotFrame = self.builder.get_object('plotFrame')
        
        localTemperatureBtn.config(text="Temperature: " + utils.getWttr(TEMPERATUREQUERY))
        localHumidityBtn.config(text="Humidity: " + utils.getWttr(HUMIDITYQUERY))
        localPrecipitationBtn.config(text="Precipitation: " + utils.getWttr(PRECIPITATIONQUERY))
        localName.config(text=LOCAL_CITY_NAME)
        weatherIcon.config(text=utils.getWttr(WCONDITIONQUERY), font=("Arial", 15))

        fcontainer = builder.get_object('plotFrame')
        self.figure = fig = Figure(figsize=(5, 4),dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=fcontainer)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        builder.connect_callbacks(self)
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

    def tempBtn(self):
        self.figure.clear()
        a = self.figure.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],data["temp"])
        self.canvas.draw()
    def humBtn(self):
        self.figure.clear()
        a = self.figure.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],data["rhum"])
        self.canvas.draw()
    def precBtn(self):
        self.figure.clear()
        a = self.figure.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],data["prcp"])
        self.canvas.draw()
        
    def optionsBtn(self):
        messagebox.showinfo(title="Impostazioni", message="Hai aperto le impostazioni")
        
    def infoBtn(self):
        messagebox.showinfo(title="Informazioni", message="Hai aperto le informazioni")
       

    def gitBtn(self):
        webbrowser.open_new(r"https://github.com/Sgambe33/PWeather")
        
root = Tk()
app = Application(root)
root.mainloop()
