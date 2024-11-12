from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import json

class ScenarioManager:
    def __init__(self):
        self.scenarios: Dict[str, dict] = {}
        self.metadata: Dict[str, dict] = {}
        self.ensembles: Dict[str, List[str]] = {}
    
    def add_scenario(self, 
                    name: str, 
                    parameters: dict, 
                    metadata: Optional[dict] = None) -> None:

        if metadata is None:
            metadata = {
                'created_at': datetime.now(),
                'version': '1.0'
            }
            
        self.scenarios[name] = parameters
        self.metadata[name] = metadata

    def create_ensemble(self,
                       base_scenario: str,
                       parameter_ranges: Dict[str, Tuple[float, float]],
                       n_members: int = 10,
                       sampling: str = 'random',
                       ensemble_name: Optional[str] = None) -> List[str]:

        base_params = self.scenarios[base_scenario].copy()
        ensemble_members = []
        
        # Generate samples
        if sampling == 'latin':
            samples = self._latin_hypercube_sampling(parameter_ranges, n_members)
        else:
            samples = self._random_sampling(parameter_ranges, n_members)
        
        # Create ensemble members
        for i, sample in enumerate(samples):
            member_name = f"{base_scenario}_member_{i}"
            member_params = base_params.copy()
            
            for (param_name, _), value in zip(parameter_ranges.items(), sample):
                member_params[param_name] = value
            
            self.add_scenario(member_name, member_params)
            ensemble_members.append(member_name)
        
        if ensemble_name:
            self.ensembles[ensemble_name] = ensemble_members
        
        return ensemble_members

    def analyze_sensitivity(self,
                          base_scenario: str,
                          parameter: str,
                          value_range: Tuple[float, float],
                          n_points: int = 10) -> Dict:
        base_params = self.scenarios[base_scenario].copy()
        values = np.linspace(value_range[0], value_range[1], n_points)
        results = []
        
        for value in values:
            params = base_params.copy()
            params[parameter] = value
            model = ClimSim(**params)
            result = model.get_variable_data('temperature').mean()
            results.append(result)
        
        return {
            'values': values,
            'results': results,
            'gradient': np.gradient(results, values)
        }

    def combine_scenarios(self,
                         scenarios: List[str],
                         weights: Optional[List[float]] = None,
                         name: Optional[str] = None) -> str:

        if weights is None:
            weights = [1.0 / len(scenarios)] * len(scenarios)
        
        combined_params = {}
        for param in self.scenarios[scenarios[0]].keys():
            values = [self.scenarios[s][param] for s in scenarios]
            combined_params[param] = np.average(values, weights=weights)
        
        if name is None:
            name = f"combined_{'_'.join(scenarios)}"
        
        self.add_scenario(name, combined_params)
        return name

    def plot_comparison(self,
                       scenarios: List[str],
                       variable: str = 'temperature',
                       years: Optional[Tuple[int, int]] = None) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for scenario in scenarios:
            model = ClimSim(**self.scenarios[scenario])
            data = model.get_variable_data(variable)
            if years:
                data = data.sel(time=slice(*years))
            data.plot(ax=ax, label=scenario)
        
        ax.set_title(f"{variable.capitalize()} Comparison")
        ax.legend()
        return fig

    def export_scenarios(self, filename: str):
        export_data = {
            'scenarios': self.scenarios,
            'metadata': self.metadata,
            'ensembles': self.ensembles
        }
        with open(f"{filename}.json", 'w') as f:
            json.dump(export_data, f, default=str)

    def _latin_hypercube_sampling(self, ranges: Dict, n_samples: int) -> np.ndarray:
        n_params = len(ranges)
        result = np.zeros((n_samples, n_params))
        
        for j, (_, (low, high)) in enumerate(ranges.items()):
            cut = np.linspace(0, 1, n_samples + 1)
            perm = np.random.permutation(n_samples)
            result[:, j] = [np.random.uniform(cut[i], cut[i+1]) 
                           for i in perm]
            result[:, j] = result[:, j] * (high - low) + low
        
        return result

    def _random_sampling(self, ranges: Dict, n_samples: int) -> np.ndarray:
        n_params = len(ranges)
        result = np.zeros((n_samples, n_params))
        
        for j, (_, (low, high)) in enumerate(ranges.items()):
            result[:, j] = np.random.uniform(low, high, n_samples)
        
        return result
