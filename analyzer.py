class ClimateAnalyzer:
    def __init__(self, model: ClimSim):
        self.model = model
        self.analysis_cache = {}
    
    def compute_trends(self, 
                      variable: str,
                      start_year: int,
                      end_year: int,
                      method: str = 'linear') -> dict:
        """
        Enhanced trend analysis with multiple methods.
        Methods: 'linear', 'polynomial', 'moving_average'
        """
        data = self.model.get_variable_data(variable, start_year, end_year)
        
        if method == 'linear':
            return self._compute_linear_trend(data)
        elif method == 'polynomial':
            return self._compute_polynomial_trend(data)
        elif method == 'moving_average':
            return self._compute_moving_average(data)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def analyze_extremes(self, 
                        variable: str,
                        threshold: Union[float, str],
                        duration: int = 1) -> dict:
        """
        Enhanced extreme event analysis with duration consideration.
        threshold can be float or 'percentile_95'
        """
        data = self.model.get_variable_data(variable)
        
        if isinstance(threshold, str) and threshold.startswith('percentile'):
            percentile = float(threshold.split('_')[1])
            threshold_value = np.percentile(data, percentile)
        else:
            threshold_value = threshold
        
        extremes = self._find_extreme_events(data, threshold_value, duration)
        
        return {
            'frequency': extremes['frequency'],
            'spatial_distribution': extremes['spatial'],
            'duration_statistics': extremes['duration'],
            'trend': extremes['trend']
        }
    
    def compute_correlations(self, 
                           variables: List[str],
                           method: str = 'pearson') -> pd.DataFrame:
        """Compute correlations between multiple climate variables."""
        data_dict = {}
        for var in variables:
            data_dict[var] = self.model.get_variable_data(var)
        
        df = pd.DataFrame(data_dict)
        return df.corr(method=method)
    
    def perform_decomposition(self, 
                            variable: str,
                            components: List[str]) -> dict:
        """
        Decompose climate signal into components.
        Components: 'trend', 'seasonal', 'residual'
        """
        data = self.model.get_variable_data(variable)
        result = {}
        
        if 'trend' in components:
            result['trend'] = self._extract_trend(data)
        if 'seasonal' in components:
            result['seasonal'] = self._extract_seasonal(data)
        if 'residual' in components:
            result['residual'] = self._extract_residual(data)
        
        return result
