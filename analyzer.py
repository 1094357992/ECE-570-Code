import numpy as np
from scipy import stats

class ClimateAnalyzer:
    def __init__(self, model: ClimSim):
        self.model = model
    
    def compute_trends(self, variable: str, start_year: int, end_year: int):
        data = self.model.get_variable_data(variable, start_year, end_year)
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            np.arange(len(data)), data.mean(dim=['lat', 'lon']))
        return {
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'std_err': std_err
        }
    
    def analyze_extremes(self, variable: str, threshold: float):
        data = self.model.get_variable_data(variable)
        extremes = data > threshold
        return {
            'frequency': extremes.mean().item(),
            'spatial_distribution': extremes.mean(dim='time')
        }
