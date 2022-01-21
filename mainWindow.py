from datetime import *
import tkinter as tk  # for python 3
from tkinter import messagebox
import pygubu
import utils
from meteostat import *
from tkinter import *

class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('mainwindow.ui')
        self.mainwindow = builder.get_object('frame1', master)
        
        fps_lable = self.builder.get_object('label3')
        ipdata = utils.getLocationFromIP()
        fps_lable.config(text=ipdata['city']) 
        
        builder.connect_callbacks(self)

    def lstWeekBtn(self):
        start = datetime.today() - timedelta(days=7)
        end = datetime.today() 
        ipData = utils.getLocationFromIP()
        data = Daily(utils.getStationIdWithIp(ipData), start, end )
        data = data.fetch() 
        messagebox.showinfo(title="Ultima settimana", message=str(data))   
        
    def weatherForecastBtn(self):
        messagebox.showinfo(title="Previsioni meteo", message="Ecco le previsioni")
        
    def weatherRecordsBtn(self):
        messagebox.showinfo(title="Archivi dati", message="Ecco gli archivi dati")
        
    def optionsBtn(self):
        messagebox.showinfo(title="Impostazioni", message="Hai aperto le impostazioni")
        
root = tk.Tk()
app = Application(root)
  
root.mainloop()
