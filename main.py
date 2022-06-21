from ScenarioManager import ScenarioManager
from ScenarioSimulator import ScenarioSimulator
from db.DBHandler import DBHandler

if __name__ == "__main__":
    db_handler = DBHandler()
    start_year = 2017
    is_benchmark = True
    num_simulations = 100
    years_to_simulate = 5

    s = ScenarioSimulator(db_handler, start_year, is_benchmark=True)
    sm = ScenarioManager(db_handler=db_handler, start_year=start_year, years_to_simulate=years_to_simulate,
                         num_simulations=num_simulations, is_benchmark=is_benchmark)
    sm.simulate_scenarios()
