import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from climsim import ClimSim

class ClimateVisualizer:
    def __init__(self, model: ClimSim):
        self.model = model
        self.data = None
        
    def plot_temperature_distribution(self, year: int):
        temp_data = self.model.get_temperature(year)
        plt.figure(figsize=(12, 6))
        sns.heatmap(temp_data, cmap='RdBu_r', center=0)
        plt.title(f'Global Temperature Distribution - Year {year}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        return plt.gcf()
    
    def plot_time_series(self, variable: str, region: tuple = None):
        data = self.model.get_variable_data(variable)
        if region:
            lat_min, lat_max, lon_min, lon_max = region
            data = data.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
        
        plt.figure(figsize=(10, 5))
        data.mean(dim=['lat', 'lon']).plot()
        plt.title(f'{variable} Time Series')
        return plt.gcf()
