class ScenarioManager:
    def __init__(self):
        self.scenarios = {}
        self.combinations = {}
        self.metadata = {}
    
    def add_scenario(self, 
                    name: str,
                    parameters: dict,
                    metadata: Optional[dict] = None):
        self.scenarios[name] = parameters
        if metadata:
            self.metadata[name] = metadata
    
    def create_ensemble(self, 
                       base_scenario: str,
                       parameter_ranges: dict,
                       n_members: int = 10) -> List[str]:
        base_params = self.scenarios[base_scenario].copy()
        ensemble_members = []
        
        for i in range(n_members):
            member_name = f"{base_scenario}_member_{i}"
            member_params = base_params.copy()
            
            for param, (min_val, max_val) in parameter_ranges.items():
                member_params[param] = np.random.uniform(min_val, max_val)
            
            self.add_scenario(member_name, member_params)
            ensemble_members.append(member_name)
        
        return ensemble_members
    
    def combine_scenarios(self, 
                         scenarios: List[str],
                         weights: Optional[List[float]] = None) -> str:
        if weights is None:
            weights = [1.0 / len(scenarios)] * len(scenarios)
        
        combined_params = {}
        for scenario, weight in zip(scenarios, weights):
            params = self.scenarios[scenario]
            for key, value in params.items():
                if key not in combined_params:
                    combined_params[key] = 0
                combined_params[key] += value * weight
        
        combined_name = f"combined_{'_'.join(scenarios)}"
        self.scenarios[combined_name] = combined_params
        return combined_name
