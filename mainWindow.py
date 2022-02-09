from datetime import *
import tkinter as tk  # for python 3
from tkinter import messagebox
import pygubu
from PIL import ImageTk, Image
import utils
from meteostat import *
from tkinter import *

class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('mainwindow.ui')
        self.mainwindow = builder.get_object('frame1', master)

        
        localName = self.builder.get_object('localName')
        weatherIconLabel = self.builder.get_object('weatherIconLabel')

        ipdata = utils.getLocationFromIP()
        localName.config(text=ipdata['city']) 

        img = Image.open("C:\\Users\\Cosimo\\Desktop\\PyMeteo\\sun.png")
        img.show()
        photo1 = ImageTk.PhotoImage(file="C:\\Users\\Cosimo\\Desktop\\PyMeteo\\sun.png")
        weatherIconLabel.configure(image=photo1)
        weatherIconLabel.photo = photo1

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
