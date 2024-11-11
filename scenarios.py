class ScenarioManager:
    def __init__(self):
        self.scenarios = {}
    
    def add_scenario(self, name: str, parameters: dict):
        self.scenarios[name] = parameters
    
    def compare_scenarios(self, scenario1: str, scenario2: str, variable: str):
        model1 = ClimSim(**self.scenarios[scenario1])
        model2 = ClimSim(**self.scenarios[scenario2])
        
        data1 = model1.get_variable_data(variable)
        data2 = model2.get_variable_data(variable)
        
        difference = data2 - data1
        return difference
