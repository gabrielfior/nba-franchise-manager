from ScenarioManager import ScenarioManager
from db.DBHandler import DBHandler


def main():
    db_handler = DBHandler()
    ######
    # Benchmark
    start_year = 2017  # should always begin 2021 if not benchmark, if yes then 2017
    is_benchmark = False
    num_simulations = 1
    years_to_simulate = 2

    ### Not benchmark
    start_year = 2021  # should always begin 2021 if not benchmark, if yes then 2017
    is_benchmark = False
    num_simulations = 2
    years_to_simulate = 3

    sm = ScenarioManager(db_handler=db_handler, start_year=start_year, years_to_simulate=years_to_simulate,
                         num_simulations=num_simulations, is_benchmark=is_benchmark)
    sm.simulate_scenarios()


if __name__ == "__main__":
    main()
