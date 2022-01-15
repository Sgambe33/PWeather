from utils import *
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

def main():
    def getCityName():
        ipdata = getLocationFromIP()
        return ipdata['city']

    root = tk.Tk()
    root.title("PyMeteo")
    root.geometry('700x400')
    root.configure(background='white')

    cityname_font = tkFont.Font(family='Calibri', size=30)

    mainframe = Frame(root, height=400, width=500, bg='lightblue')
    mainframe.pack_propagate(False) 
    mainframe.pack(side=LEFT)

    citynameLabel = Label(mainframe, text=getCityName(), font=cityname_font )
    citynameLabel.pack()

    root.mainloop()
    pass
if __name__ == "__main__":
    main()