from datetime import *
from mmap import mmap
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from tkinter import *
from pandastable import Table
from meteostat import Hourly, Daily, Monthly
from tkcalendar import Calendar, DateEntry

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

    def run(self):
        self.mainwindow.mainloop()

    def onHourlyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        data = Hourly(utils.getStationIdWithCityName(cityNameLabel.get()), start, end )
        data = data.fetch()
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()
    
    def onDailyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        data = Daily(utils.getStationIdWithCityName(cityNameLabel.get()), start, end )
        data = data.fetch()
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()

    def onMonthlyFetchButtonClick(self):
        calendarStart = self.builder.get_object('calendarStart')
        calendarEnd = self.builder.get_object('calendarEnd')
        csv_frame = self.builder.get_object('csvFrame')
        cityNameLabel = self.builder.get_object('localityInput')
        errorLabel = self.builder.get_object('outputLabel')
        start = datetime.combine(calendarStart.get_date(), datetime.min.time())
        end = datetime.combine(calendarEnd.get_date(), datetime.max.time())
        try:
            data = Monthly(utils.getStationIdWithCityName(cityNameLabel.get()), start, end)
            data = data.fetch()
        except:
            errorLabel.config(text="Internet connection error!")
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True, width=690, height=400)
        pt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = RecordsViewerApp(root)
    app.run()
