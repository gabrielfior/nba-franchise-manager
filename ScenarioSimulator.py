import uuid
from dataclasses import dataclass

from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from LotteryCoordinator import LotteryCoordinator
from PlayoffCoordinator import PlayoffCoordinator
from ScheduleSimulator import ScheduleSimulator
from StandingsCalculator import StandingsCalculator
from db.DBHandler import DBHandler


@dataclass
class ScenarioSimulator:

    def __init__(self, db_handler: DBHandler, start_year: int):
        self.db_handler = db_handler
        self.start_year = start_year

        self.simulation_id = str(uuid.uuid4())

    def simulate_scenario(self, n_years):
        for year in range(n_years):
            self.simulate_year(self.start_year + year)

    def simulate_year(self, year: int):
        draft_simulator = DraftSimulator(self.db_handler, year, self.simulation_id)
        draft_simulator.simulate_draft()

        game_simulator = GameSimulator(self.db_handler, self.simulation_id)

        ScheduleSimulator(self.db_handler, year, simulation_id=self.simulation_id).generate_schedule()
        game_simulator.simulate_reg_season()
        StandingsCalculator(self.db_handler, self.simulation_id, year).calculate_standings()
        PlayoffCoordinator(self.db_handler, self.simulation_id, year, game_simulator).simulate_playoffs()
        LotteryCoordinator(self.db_handler, self.simulation_id).generate_lottery(year)
