import numpy as np
from scipy import stats

class ClimateAnalyzer:
    def __init__(self, model: ClimSim):
        self.model = model
    
    def compute_trends(self, variable: str, start_year: int, end_year: int):
        """Compute linear trends in climate variables."""
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
        """Analyze extreme events in climate data."""
        data = self.model.get_variable_data(variable)
        extremes = data > threshold
        return {
            'frequency': extremes.mean().item(),
            'spatial_distribution': extremes.mean(dim='time')
        }

# scenarios.py
class ScenarioManager:
    def __init__(self):
        self.scenarios = {}
    
    def add_scenario(self, name: str, parameters: dict):
        """Add a new climate scenario."""
        self.scenarios[name] = parameters
    
    def compare_scenarios(self, scenario1: str, scenario2: str, variable: str):
        """Compare two climate scenarios."""
        model1 = ClimSim(**self.scenarios[scenario1])
        model2 = ClimSim(**self.scenarios[scenario2])
        
        data1 = model1.get_variable_data(variable)
        data2 = model2.get_variable_data(variable)
        
        difference = data2 - data1
        return difference
