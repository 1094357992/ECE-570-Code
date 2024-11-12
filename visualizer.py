import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
from typing import Union, Tuple, List, Optional

class ClimateVisualizer:
    def __init__(self, model: ClimSim):
        self.model = model
        self.data = None
        self.projection = ccrs.PlateCarree()
        self.style_config = {
            'cmap': 'RdBu_r',
            'figsize': (12, 6),
            'dpi': 100
        }
    
    def set_style(self, **kwargs):
        self.style_config.update(kwargs)
    
    def plot_temperature_distribution(self, 
                                    year: int,
                                    overlay_features: bool = False) -> plt.Figure:
        temp_data = self.model.get_temperature(year)
        
        fig = plt.figure(figsize=self.style_config['figsize'])
        ax = fig.add_subplot(1, 1, 1, projection=self.projection)
        
        if overlay_features:
            ax.coastlines()
            ax.gridlines()
        
        img = ax.contourf(temp_data, 
                         cmap=self.style_config['cmap'],
                         transform=self.projection)
        plt.colorbar(img, label='Temperature (°C)')
        
        return fig
    
    def create_animation(self, 
                        variable: str,
                        start_year: int,
                        end_year: int,
                        fps: int = 10) -> FuncAnimation:
        fig = plt.figure(figsize=self.style_config['figsize'])
        ax = fig.add_subplot(1, 1, 1, projection=self.projection)
        
        def update(frame):
            ax.clear()
            data = self.model.get_variable_data(variable, frame)
            img = ax.contourf(data, transform=self.projection)
            ax.set_title(f'Year: {frame}')
            return [img]
        
        years = range(start_year, end_year + 1)
        anim = FuncAnimation(fig, update, frames=years, interval=1000//fps)
        return anim
    
    def plot_multiple_variables(self, 
                              variables: List[str],
                              year: int,
                              region: Optional[Tuple] = None) -> plt.Figure:
        n_vars = len(variables)
        fig, axes = plt.subplots(1, n_vars, 
                                figsize=(6*n_vars, 6),
                                subplot_kw={'projection': self.projection})
        
        for ax, var in zip(axes, variables):
            data = self.model.get_variable_data(var, year)
            if region:
                data = self._filter_region(data, region)
            img = ax.contourf(data, transform=self.projection)
            ax.set_title(var.capitalize())
            plt.colorbar(img, ax=ax)
        
        return fig
    
    def plot_seasonal_comparison(self, 
                               variable: str,
                               year: int) -> plt.Figure:
        """Plot seasonal comparisons of climate variables."""
        seasons = ['DJF', 'MAM', 'JJA', 'SON']
        fig, axes = plt.subplots(2, 2, figsize=(15, 15),
                                subplot_kw={'projection': self.projection})
        
        for ax, season in zip(axes.flat, seasons):
            data = self.model.get_seasonal_data(variable, year, season)
            img = ax.contourf(data, transform=self.projection)
            ax.set_title(f'{season} {year}')
            plt.colorbar(img, ax=ax)
        
        return fig
