import pandas as pd
import xarray as xr

class DataExporter:
    @staticmethod
    def to_csv(data: xr.DataArray, filename: str):
        df = data.to_dataframe()
        df.to_csv(filename)
    
    @staticmethod
    def to_netcdf(data: xr.DataArray, filename: str):
        data.to_netcdf(filename)
    
    @staticmethod
    def create_report(analyzer: ClimateAnalyzer, scenarios: list, variables: list):
        report = pd.DataFrame()
        for scenario in scenarios:
            for variable in variables:
                trends = analyzer.compute_trends(variable, 2020, 2100)
                report = report.append({
                    'scenario': scenario,
                    'variable': variable,
                    **trends
                }, ignore_index=True)
        return report
