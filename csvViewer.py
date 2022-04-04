from datetime import *
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from tkinter import *
from pandastable import Table
from meteostat import Hourly
from tkcalendar import Calendar, DateEntry


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
        
    def onFetchButtonClick(self):
        calendario = self.builder.get_object('calendar1')
        csv_frame = self.builder.get_object('csvFrame')
        print(calendario.get_date())
        start = datetime.now() - timedelta(hours=24)
        end = datetime.now()
        data = Hourly('72219', start, end )
        data = data.fetch()
        pt = Table(parent=csv_frame, dataframe=data, showtoolbar=True, showstatusbar=True)
        pt.show()







if __name__ == '__main__':
    root = tk.Tk()
    app = RecordsViewerApp(root)
    app.run()


