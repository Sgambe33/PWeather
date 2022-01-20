import tkinter as tk  # for python 3
from tkinter import messagebox
import pygubu
import utils
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
        messagebox.showinfo(title="Ultima settimana", message="Ecco il meteo dell'ultima settimana")   
        
    def weatherForecastBtn(self):
        messagebox.showinfo(title="Previsioni meteo", message="Ecco le previsioni")
        
    def weatherRecordsBtn(self):
        messagebox.showinfo(title="Archivi dati", message="Ecco gli archivi dati")
        
    def optionsBtn(self):
        messagebox.showinfo(title="Impostazioni", message="Hai aperto le impostazioni")
        
root = tk.Tk()
app = Application(root)
  
root.mainloop()
