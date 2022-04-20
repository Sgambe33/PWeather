import os
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import pygubu


class MyApplication:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        uifile = os.path.join(os.path.dirname(__file__),"issue145.ui")
        builder.add_from_file(uifile)

        self.mainwindow = builder.get_object('mainwindow')
        
        # Container for the matplotlib canvas and toolbar classes
        fcontainer = builder.get_object('fcontainer')
        
        # Setup matplotlib canvas
        self.figure = fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=fcontainer)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Setup matplotlib toolbar (optional)
        self.toolbar = NavigationToolbar2Tk(canvas, fcontainer)
        self.toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Connect button callback
        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()
        
    def on_plot_clicked(self):
        a = self.figure.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        self.canvas.draw()


if __name__ == '__main__':
    app = MyApplication()
    app.run()