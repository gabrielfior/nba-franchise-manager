import uuid
from dataclasses import dataclass

from DraftPickManager import DraftPickManager
from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from Logger import Logger
from LotteryCoordinator import LotteryCoordinator
from PlayerExpander import PlayerExpander
from PlayerManager import PlayerManager
from PlayoffCoordinator import PlayoffCoordinator
from ScheduleSimulator import ScheduleSimulator
from StandingsCalculator import StandingsCalculator
from TradeManager import TradeManager
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

        PlayerManager(self.db_handler, self.simulation_id).duplicate_entities_without_sim_id()
        DraftPickManager(self.db_handler, self.simulation_id).duplicate_entities_without_sim_id()
        if not self.is_benchmark:
            # Copy player stats to subsequent years
            PlayerExpander(self.db_handler, self.simulation_id, self.start_year, n_years).expand_entities()

        for year in range(n_years):
            year_to_simulate = self.start_year + year
            self.logger.logger.info("Simulating year {} simulation_id {}".format(year_to_simulate, self.simulation_id))
            self.simulate_year(year_to_simulate)

    def simulate_year(self, year: int):

        if not self.is_benchmark:
            draft_simulator = DraftSimulator(self.db_handler, year, self.simulation_id)
            self.logger.logger.info('Starting simulate draft')
            draft_simulator.simulate_draft()

        TradeManager(self.db_handler, self.simulation_id, year).execute_trades()

        self.logger.logger.info('Starting schedule simulator')
        ScheduleSimulator(self.db_handler, year, simulation_id=self.simulation_id).generate_schedule()
        game_simulator = GameSimulator(self.db_handler, self.simulation_id)
        self.logger.logger.info('Starting game simulator')
        game_simulator.simulate_game_type(self.simulation_id, year, GameTypes.REGULAR_SEASON)
        self.logger.logger.info('Starting standings simulator')
        StandingsCalculator(self.db_handler, self.simulation_id, year).calculate_standings()
        self.logger.logger.info('Starting playoff simulator')
        PlayoffCoordinator(self.db_handler, self.simulation_id, year, game_simulator).simulate_playoffs()

        if not self.is_benchmark:
            self.logger.logger.info('Starting lottery simulator')
            LotteryCoordinator(self.db_handler, self.simulation_id, year).generate_lottery()
