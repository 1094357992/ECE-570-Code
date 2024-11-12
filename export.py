class DataExporter:
    @staticmethod
    def to_csv(data: xr.DataArray,
               filename: str,
               compression: Optional[str] = None):
        """Export to CSV with compression options."""
        df = data.to_dataframe()
        if compression:
            filename = f"{filename}.{compression}"
            df.to_csv(filename, compression=compression)
        else:
            df.to_csv(filename)
    
    @staticmethod
    def to_netcdf(data: xr.DataArray,
                  filename: str,
                  encoding: Optional[dict] = None):
        """Export to NetCDF with encoding options."""
        if encoding:
            data.to_netcdf(filename, encoding=encoding)
        else:
            data.to_netcdf(filename)
    
    @classmethod
    def create_report(cls,
                     analyzer: ClimateAnalyzer,
                     scenarios: List[str],
                     variables: List[str],
                     report_type: str = 'full') -> Union[pd.DataFrame, dict]:
 
        if report_type == 'full':
            return cls._create_full_report(analyzer, scenarios, variables)
        elif report_type == 'summary':
            return cls._create_summary_report(analyzer, scenarios, variables)
        elif report_type == 'trends':
            return cls._create_trends_report(analyzer, scenarios, variables)
        elif report_type == 'extremes':
            return cls._create_extremes_report(analyzer, scenarios, variables)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
    
    @staticmethod
    def export_visualization(fig: plt.Figure,
                           filename: str,
                           format: str = 'png',
                           **kwargs):
        fig.savefig(f"{filename}.{format}", **kwargs)
    
    @staticmethod
    def create_dashboard(data: dict,
                        template: str = 'basic') -> str:
        if template == 'basic':
            return cls._create_basic_dashboard(data)
        elif template == 'advanced':
            return cls._create_advanced_dashboard(data)
        else:
            raise ValueError(f"Unknown template: {template}")
