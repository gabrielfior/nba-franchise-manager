import uuid
from dataclasses import dataclass

from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from Logger import Logger
from LotteryCoordinator import LotteryCoordinator
from PlayoffCoordinator import PlayoffCoordinator
from ScheduleSimulator import ScheduleSimulator
from StandingsCalculator import StandingsCalculator
from db.DBHandler import DBHandler
from enums import GameTypes


@dataclass
class ScenarioSimulator:
    db_handler: DBHandler
    start_year: int
    is_benchmark: bool = False
    logger = Logger()

    def __post_init__(self):
        self.simulation_id = str(uuid.uuid4())

    def simulate_scenario(self, n_years):
        for year in range(n_years):
            year_to_simulate = self.start_year + year
            self.logger.logger.info("Simulating year {} simulation_id {}".format(year_to_simulate, self.simulation_id))
            self.simulate_year(year_to_simulate)

    def simulate_year(self, year: int):
        if not self.is_benchmark:
            draft_simulator = DraftSimulator(self.db_handler, year, self.simulation_id)
            draft_simulator.simulate_draft()

        ScheduleSimulator(self.db_handler, year, simulation_id=self.simulation_id).generate_schedule()
        game_simulator = GameSimulator(self.db_handler, self.simulation_id)
        game_simulator.simulate_game_type(self.simulation_id, year, GameTypes.REGULAR_SEASON)
        StandingsCalculator(self.db_handler, self.simulation_id, year).calculate_standings()
        PlayoffCoordinator(self.db_handler, self.simulation_id, year, game_simulator).simulate_playoffs()

        if not self.is_benchmark:
            LotteryCoordinator(self.db_handler, self.simulation_id).generate_lottery(year)
