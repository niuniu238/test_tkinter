import numpy as np
import tkinter as tk
# import tkinter.filedialog
# import rasterio
# import rioxarray as rxr
import xarray as xr
from tkcalendar import DateEntry
from dateutil import parser
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
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
        
        data = self.read_nc()

        HunanProvince_shp_path = 'shp/Hunan_province..shp'
        Hunan_shp_path = '/home/xbb/Code/python/Hunan_E/shp/Hunan_city.shp'
        EW_shp_path = '/home/xbb/Code/python/Hunan_E/shp/electric_wire.shp'

        Hunan_c = Reader(Hunan_shp_path)
        Hunan_p = Reader(HunanProvince_shp_path)
        electric_wire = Reader(EW_shp_path)

        self.fig1 = plt.figure(figsize=(6,6),dpi=100)
        self.ax1 = plt.axes(projection=ccrs.PlateCarree())
        self.ax1.set_title(self.param_var.get()+self.date_entry.get())

        self.ax1.add_geometries(electric_wire.geometries(),crs=ccrs.PlateCarree(),
                          facecolor='none',linestyle='-.',edgecolor='red',linewidth=1,zorder=2)
        self.ax1.add_geometries(Hunan_c.geometries(),crs=ccrs.PlateCarree(),
                          facecolor='none',edgecolor='black',linewidth=0.3,zorder=2)
        self.ax1.add_geometries(Hunan_p.geometries(),crs=ccrs.PlateCarree(),
                          facecolor='none',edgecolor='black',alpha=0.5,linewidth=1.5,zorder=2)

        img = self.ax1.pcolormesh(data.longitude,data.latitude,data[-1],transform=ccrs.PlateCarree()) 
        self.ax1.set_xlim(data.longitude.min(),data.longitude.max())
        self.ax1.set_ylim(data.latitude.min(),data.latitude.max())
        
        self.canvas1 = FigureCanvasTkAgg(self.fig1,master=self.frame2)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.grid(row=0, column=0)
        self.canvas1.draw()

        self.fig1.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self,event):
        # print("my position:" ,event.button,event.xdata, event.ydata)
        row,col = self.func_geo_to_imagexy(self.geotransform,event.xdata,event.ydata)
        print(row,col)
        data = self.read_nc()
        self.fig2 = plt.figure(figsize=(6,2),dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.scatter(event.xdata, event.ydata)
        self.ax2.set_ylabel('khkhkk')
        self.ax2.set_xlabel('xxxxxx')
        self.ax2.set_xlim(108.5,114.5)
        self.ax2.set_ylim(24.4,30.3)
        plt.tight_layout()
        self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.frame2)
        self.canvas_widget2 = self.canvas2.get_tk_widget()
        self.canvas_widget2.grid(row=1, column=0)
        self.canvas2.draw()

        self.fig3 = plt.figure(figsize=(4,6),dpi=100)
        self.ax3 = self.fig3.add_subplot(111)
        # self.ax3.scatter(event.xdata, event.ydata)
        self.ax3.plot(data[:,row,col]-273.15,1000-data.level,'-o')

        self.ax3.set_yticks(np.arange(0, 801, 100))
        self.ax3.set_yticklabels([str(i) for i in np.arange(1000, 199, -100)])
        self.ax3.set_ylabel('khkhkk')
        self.ax3.set_xlabel('xxxxxx')
        # self.ax3.set_xlim(108.5,114.5)
        # self.ax3.set_ylim(24.4,30.3)
        plt.tight_layout()
        self.canvas3 = FigureCanvasTkAgg(self.fig3,master=self.frame2)
        self.canvas_widget3 = self.canvas3.get_tk_widget()
        self.canvas_widget3.grid(row=0, column=1)
        self.canvas3.draw()
    # def fig
    def read_nc(self):
        # path = '/media/xbb/xbbRed/Hunan_electric/data/tif/liquid_water_2022-12-25.tif'
        # data = rxr.open_rasterio(path)
        dict_paramter = {"temperature":"t", "relative_humidity":"r", "wind":{'u':'u','v':'v'}, "liquid_water":"tclw"}
        paramter = self.param_var.get()
        date_entry = self.date_entry.get()
        path = f'data/interp_nc/interp_{paramter}.nc'
        self.ds = xr.open_dataset(path)
        date_entry_ = date_entry.replace('/','-')

        str = f'{date_entry_}T05:00:00.000000000'
        dsi = self.ds.sel(time=np.datetime64(str))

        data = dsi[dict_paramter[paramter]]
        self.func_get_transform()
        return data
    
    def func_get_transform(self):
        lon = self.ds.longitude
        lat = self.ds.latitude
        lon_min, _, _, lat_max = lon.min(), lon.max(), lat.min(), lat.max()
        res = (lon[1] - lon[0], lat[1] - lat[0])
        # 创建GeoTransform对象,注意这个数据的lat是##从小到大##排序的
        self.geotransform = (lon_min, res[0], 0, lat_max, 0, res[1])
    def func_geo_to_imagexy(self,trans,lon,lat):
        '''
        根据GDAL六参数模型将地理坐标转换为图上坐标
        return:返回图上行列号(row,col)
        '''
        x,y=lon,lat
        a = np.array([[trans[1],trans[2]],[trans[4],trans[5]]])
        b = np.array([x-trans[0],y-trans[3]])
        col,row = np.linalg.solve(a,b).astype(int)
        return row,col
    def func_imagexy_to_geo(self,trans,row,col):
        '''
        根据图上行列号转换GDAL六参数
        return:lon,lat
        '''
        lon = trans[0]+col*trans[1]+row*trans[2]
        lat = trans[3]+col*trans[4]+row*trans[5]
        return lon,lat

    
root = tk.Tk()
root.title('hello')
app = MainApplication(master=root)
app.mainloop()

