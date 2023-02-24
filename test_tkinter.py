import numpy as np
import tkinter as tk
# import tkinter.filedialog
# import rasterio
import rioxarray as rxr
from tkcalendar import DateEntry
from dateutil import parser
import cartopy.crs as ccrs
import cartopy.io.shapereader as Reader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()  
        
    def create_widgets(self):
        myfont = "Times"

         # Create a menu bar
        menubar = tk.Menu(self.master)

        # Create a file menu
        filemenu = tk.Menu(menubar, tearoff=0,font=(myfont,16))
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)

        # Add the file menu to the menu bar
        menubar.add_cascade(label="File", menu=filemenu,font=(myfont,16))

        # Configure the menu bar
        self.master.config(menu=menubar)

        # Create a frame for displaying images
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=0, column=0)

        # Add a canvas to frame2 for displaying the main image
        self.canvas1 = tk.Canvas(self.frame2, width=600, height=600, bd=2, relief='sunken')
        self.canvas1.grid(row=0, column=0)
        
        # Add a canvas to frame2 for displaying data2
        self.canvas2 = tk.Canvas(self.frame2, width=600, height=200, bd=2, relief='sunken')
        self.canvas2.grid(row=1, column=0)
    
        # Add a canvas to frame2 for displaying data3
        self.canvas3 = tk.Canvas(self.frame2, width=400, height=600, bd=2, relief='sunken')
        self.canvas3.grid(row=0, column=1)     

        # Create a frame for displaying option and button
        self.frame3 = tk.Frame(self.frame2, width=400, height=200, bd=2, relief='groove')
        self.frame3.grid(row=1, column=1)
        ############################################

        # Add some widgets to frame1 using grid
        self.date_label = tk.Label(self.frame3, text="Select a date:",font=(myfont,12))
        self.date_label.place(relx=0.1,rely=0.1)

        # Calculate the start and end dates for the date range
        start_date = parser.parse("2022-12-25")
        end_date =  parser.parse("2022-12-31")

        self.date_entry = DateEntry(self.frame3, width=12, background='darkblue', foreground='white',
                                    borderwidth=2, mindate=start_date, maxdate=end_date,font=(myfont,12))
        self.date_entry.place(relx=0.5,rely=0.1)
        print(self.date_entry.get())

        self.param_label = tk.Label(self.frame3, text="Select a parameter:",font=(myfont,12))
        self.param_label.place(relx=0.1,rely=0.4)

        self.param_options = ["temperature", "relative_humidity", "wind", "liquid_water"]
        self.param_var = tk.StringVar()
        self.param_var.set(self.param_options[0])

        self.param_dropdown = tk.OptionMenu(self.frame3, self.param_var, *self.param_options,)
        self.param_dropdown.config(width=18,)
        self.param_dropdown.place(relx=0.5,rely=0.39)
        # self.param_var.get()

        # Add a button to load image data
        self.load_button = tk.Button(self.frame3, text="Load Data", command=self.load_data,)
        # self.load_button.grid(row=0, column=0,padx=10,pady=10)
        self.load_button.place(relx=0.4,rely=0.8,)
        
    def load_data(self):
        
        data = self.read_tif()
        fig = plt.figure(figsize=(6,6),dpi=100)
        plt.title(self.param_var.get()+self.date_entry.get())

        ax = plt.axes(projection=ccrs.PlateCarree())
        img = ax.pcolormesh(data.x,data.y,data[0],transform=ccrs.PlateCarree()) 
        canvas1 = FigureCanvasTkAgg(fig,master=self.frame2)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.grid(row=0, column=0)
        canvas1.draw()
        #  TODO: Load image data and display on canvas1
        pass
        # TODO: Load data2 and display on canvas2
        pass
        # TODO: Load data3 and display on canvas3
        pass
    def read_tif(self):
        path = 'data/tif/liquid_water_2022-12-25.tif'
        # ./../data/tif/liquid_water_2022-12-25.tif
        data = rxr.open_rasterio(path)

        return data

root = tk.Tk()
root.title('hello')
app = MainApplication(master=root)
app.mainloop()

