import uuid

from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from PlayoffCoordinator import PlayoffCordinator
from ScenarioSimulator import ScenarioSimulator
from ScheduleSimulator import ScheduleSimulator
from StandingsCalculator import StandingsCalculator
from db.DBHandler import DBHandler

if __name__ == "__main__":

    db_handler = DBHandler()
    draft_year = 2021

    simulation_id = str(uuid.uuid4())
    print ('simulating ID {}'.format(simulation_id))

    draft_simulator = DraftSimulator(db_handler, draft_year)
    s = ScenarioSimulator(draft_simulator)
    s.simulate_scenario(1)
    d = ScheduleSimulator(db_handler, draft_year, simulation_id=simulation_id)
    d.generate_schedule()

    g = GameSimulator(simulation_id,db_handler)
    g.simulate_reg_season()

    sc = StandingsCalculator(db_handler, simulation_id, draft_year)
    sc.calculate_standings()

    game_simulator = GameSimulator(simulation_id, db_handler)
    pc = PlayoffCordinator(db_handler, simulation_id, draft_year, game_simulator)
    pc.simulate_playoffs()

    print ('done')