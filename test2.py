import tkinter as tk
import tkinter.filedialog
import rasterio
import xarray as xr


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for date and parameter selection
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row=0, column=0, columnspan=2)

        # Add some widgets to frame1 using grid
        self.date_label = tk.Label(self.frame1, text="Select a date:")
        self.date_label.grid(row=0, column=0)

        self.date_entry = tk.Entry(self.frame1)
        self.date_entry.grid(row=0, column=1)

        self.param_label = tk.Label(self.frame1, text="Select a parameter:")
        self.param_label.grid(row=0, column=2)

        self.param_options = ["Parameter 1", "Parameter 2", "Parameter 3"]
        self.param_var = tk.StringVar()
        self.param_var.set(self.param_options[0])

        self.param_dropdown = tk.OptionMenu(self.frame1, self.param_var, *self.param_options)
        self.param_dropdown.grid(row=0, column=3)

        # Create a frame for displaying images
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=1, column=0)

        # Add a canvas to frame2 for displaying the main image
        self.canvas1 = tk.Canvas(self.frame2, width=800, height=600, bd=2, relief='sunken')
        self.canvas1.grid(row=0, column=0)

        # Add a canvas to frame2 for displaying data2
        self.canvas2 = tk.Canvas(self.frame2, width=800, height=200, bd=2, relief='sunken')
        self.canvas2.grid(row=1, column=0)
  
        # Add a canvas to frame2 for displaying data3
        self.canvas3 = tk.Canvas(self.frame2, width=200, height=600, bd=2, relief='sunken')
        self.canvas3.grid(row=0, column=1)

        # Add a button to load image data
        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.grid(row=2, column=0)

    def load_data(self):
        # TODO: Load image data and display on canvas1
        pass
        # TODO: Load data2 and display on canvas2
        pass
        # TODO: Load data3 and display on canvas3
        pass

root = tk.Tk()
app = MainApplication(master=root)
app.mainloop()
