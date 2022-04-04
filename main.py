import uuid

from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from ScenarioSimulator import ScenarioSimulator
from ScheduleSimulator import ScheduleSimulator
from StandingsCalculator import StandingsCalculator
from db.DBHandler import DBHandler

if __name__ == "__main__":

    db_handler = DBHandler()
    draft_year = 2021
    '''
    simulation_id = str(uuid.uuid4())
    print ('simulating ID {}'.format(simulation_id))

    draft_simulator = DraftSimulator(db_handler, draft_year)
    s = ScenarioSimulator(draft_simulator)
    s.simulate_scenario(1)
    d = ScheduleSimulator(db_handler, draft_year, simulation_id=simulation_id)
    d.generate_schedule()

    # ToDo - simulate games
    g = GameSimulator(simulation_id,db_handler)
    g.simulate()

    # ToDo - get standings from regular season
    # ToDo - simulate final games
    '''
    simulation_id = 'f4c4797e-42e9-451b-9284-d95f5559a89b'
    sc = StandingsCalculator(db_handler, simulation_id, draft_year)
    sc.calculate_standings()
    print ('oi')