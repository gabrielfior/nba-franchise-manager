from DraftSimulator import DraftSimulator
from ScenarioSimulator import ScenarioSimulator
from ScheduleSimulator import ScheduleSimulator

from db.DBHandler import DBHandler

if __name__ == "__main__":
    db_handler = DBHandler()
    draft_year = 0
    #draft_simulator = DraftSimulator(db_handler, draft_year)
    #s = ScenarioSimulator(draft_simulator)
    #s.simulate_scenario(1)
    d = ScheduleSimulator(db_handler)
    d.generate_schedule()
    #print("DONE")
