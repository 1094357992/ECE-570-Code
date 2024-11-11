# ClimViz

A comprehensive extension for climate data visualization and analysis built on top of the ClimSim library.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

## Overview

ClimViz is a powerful Python package that extends the ClimSim library with advanced visualization and analysis capabilities. It provides researchers, scientists, and educators with tools for:

- Interactive climate data visualization
- Statistical analysis of climate trends
- Scenario comparison and management
- Data export and reporting

## Features

### 🎨 Visualization
- Temperature distribution heatmaps
- Time series analysis plots
- Regional visualization support
- Customizable plotting options

### 📊 Analysis
- Trend computation and analysis
- Extreme event detection
- Statistical significance testing
- Error estimation

### 🔄 Scenario Management
- Multiple scenario handling
- Parameter management
- Scenario comparison
- Difference analysis

### 📁 Data Export
- Multiple format support (CSV, NetCDF)
- Automated report generation
- Summary statistics

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/climviz.git

# Navigate to the project directory
cd climviz

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from climviz import ClimateVisualizer, ClimateAnalyzer
from climsim import ClimSim

# Initialize the model
model = ClimSim(start_year=2020, end_year=2100)

# Create visualizer
viz = ClimateVisualizer(model)

# Create temperature distribution plot
temp_plot = viz.plot_temperature_distribution(2050)
temp_plot.savefig('temperature_2050.png')

# Analyze trends
analyzer = ClimateAnalyzer(model)
trends = analyzer.compute_trends('temperature', 2020, 2100)
print(trends)
```

## Dependencies

```plaintext
climsim>=1.0.0
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
xarray>=0.20.0
```

## Documentation

### ClimateVisualizer

```python
viz = ClimateVisualizer(model)

# Create temperature distribution plot
viz.plot_temperature_distribution(year=2050)

# Create time series plot
viz.plot_time_series(
    variable='temperature',
    region=(30, 60, -130, -70)  # Optional: lat_min, lat_max, lon_min, lon_max
)
```

### ClimateAnalyzer

```python
analyzer = ClimateAnalyzer(model)

# Compute trends
trends = analyzer.compute_trends(
    variable='temperature',
    start_year=2020,
    end_year=2100
)

# Analyze extreme events
extremes = analyzer.analyze_extremes(
    variable='temperature',
    threshold=2.0
)
```

### ScenarioManager

```python
manager = ScenarioManager()

# Add scenarios
manager.add_scenario('baseline', {
    'co2_emissions': 'medium',
    'temperature_sensitivity': 1.0
})

manager.add_scenario('high_emissions', {
    'co2_emissions': 'high',
    'temperature_sensitivity': 1.2
})

# Compare scenarios
difference = manager.compare_scenarios(
    'baseline',
    'high_emissions',
    'temperature'
)
```

### DataExporter

```python
# Export to CSV
DataExporter.to_csv(data, 'output.csv')

# Export to NetCDF
DataExporter.to_netcdf(data, 'output.nc')

# Create analysis report
report = DataExporter.create_report(
    analyzer,
    ['baseline', 'high_emissions'],
    ['temperature', 'precipitation']
)
```

## Project Structure

```
climviz/
├── __init__.py      # Package initialization
├── visualizer.py    # Visualization tools
├── analyzer.py      # Statistical analysis
├── scenarios.py     # Scenario management
└── export.py        # Data export utilities
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=climviz tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use ClimViz in your research, please cite:

```bibtex
@software{climviz2024,
  author = {Your Name},
  title = {ClimViz: A Comprehensive Extension for Climate Data Visualization},
  year = {2024},
  url = {https://github.com/yourusername/climviz}
}
```

## Contact

- Email: your.email@example.com
- GitHub Issues: https://github.com/yourusername/climviz/issues

## Acknowledgments

- ClimSim development team
- Scientific Python community
- All contributors and users

