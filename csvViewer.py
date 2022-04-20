from datetime import *
from mmap import mmap
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from tkinter import messagebox
from pandastable import Table
from meteostat import Hourly, Daily, Monthly, Stations
from tkcalendar import Calendar, DateEntry
import webbrowser


import utils

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "records_viewer.ui"


class RecordsViewerApp:
    
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainFrame', master)
        builder.connect_callbacks(self)
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        calendarStart.set_date(datetime.now()-timedelta(days=1))
        calendarEnd.set_date(datetime.now())

    def run(self):
        self.mainwindow.mainloop()

    def onHourlyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        errorLabel = self.builder.get_object('outputLabel')
        errorLabel.config(text="")
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        try:
            if(cityNameLabel.get() == ""):
                errorLabel.config(text="Insert a valid locality!")
                
            else:
                data = Hourly(utils.getStationIdWithCityName(cityNameLabel.get()), start, end)
                data = data.fetch()
        except :
            errorLabel.config(text="Internet connection error!")
            
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()
    
    def onDailyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        errorLabel = self.builder.get_object('outputLabel')
        errorLabel.config(text="")
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        try:
            try:
                data = Daily(utils.getStationIdWithCityName(cityNameLabel.get()), start, end)
            except:
                errorLabel.config(text="Insert a valid locality!")
            data = data.fetch()
        except:
            errorLabel.config(text="Internet connection error!")
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()

    def onMonthlyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        errorLabel = self.builder.get_object('outputLabel')
        errorLabel.config(text="")
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        try:
            try:
                data = Monthly(utils.getStationIdWithCityName(cityNameLabel.get()), start, end)
            except:
                errorLabel.config(text="Insert a valid locality!")
            data = data.fetch()
        except:
            errorLabel.config(text="Internet connection error!")
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()
    
    def onStationShowMapsClick(self):
        cityNameLabel = self.builder.get_object('localityInput')
        errorLabel = self.builder.get_object('outputLabel')
        errorLabel.config(text="")
        stations = Stations()
        try:
            coords = utils.getPosFromCity(cityNameLabel.get())
            stations = stations.nearby(coords.latitude, coords.longitude)
            station = stations.fetch(1)
            station.reset_index(drop=True, inplace=True)
            webbrowser.open("https://www.google.com/maps/search/?api=1&query="+str(station.at[0,"latitude"])+"%2C"+str(station.at[0,"longitude"]))
        except AttributeError:
            errorLabel.config(text="No city with that name!")
    
    def infoBtn(self):
        infoMsg = " temp-->The air temperature in °C\n dwpt-->The dew point in °C\n rhum-->The relative humidity in percent (%)\n prcp-->The one hour precipitation total in mm\n snow-->The snow depth in mm\n wdir-->The wind direction in °\n wspd-->The wind speed in m/s\n wgst-->The wind gust in m/s\n pres-->The air pressure in hPa\n tsun-->The one hour sunshine total in minutes (m)\n coco-->The weather condition code"
        messagebox.showinfo(title="Info", message=infoMsg)

if __name__ == '__main__':
    root = tk.Tk()
    app = RecordsViewerApp(root)
    app.run()
