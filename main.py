import time

from ScenarioSimulator import ScenarioSimulator
from db.DBHandler import DBHandler

if __name__ == "__main__":

    start = time.time()
    db_handler = DBHandler()
    start_year = 2021

    #simulation_id = '29b61f39-a87b-42f7-864f-8bb7c11e5a18'
    #print ('simulating ID {}'.format(simulation_id))

    s = ScenarioSimulator(db_handler, start_year=start_year)
    s.simulate_scenario(2)

    print ('finished - time elapsed (s) {}'.format(time.time() - start))