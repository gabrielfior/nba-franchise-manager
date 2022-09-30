import time
import uuid
from dataclasses import dataclass

from Logger import Logger
from ScenarioSimulator import ScenarioSimulator
from db.DBHandler import DBHandler
from db.models.scenario import ScenarioDb


@dataclass
class ScenarioManager:
    db_handler: DBHandler
    start_year: int
    years_to_simulate: int
    num_simulations: int
    logger = Logger()
    is_benchmark: bool = False

    def __post_init__(self):
        self.scenario_group_id = str(uuid.uuid4())

    def simulate_scenarios(self):
        start = time.time()
        self.logger.logger.info("Simulating scenario group {}".format(self.scenario_group_id))


        for simulation_idx in range(self.num_simulations):
            self.logger.logger.debug(f'simulation # {simulation_idx} / {self.num_simulations}')

            s = ScenarioSimulator(self.db_handler, start_year=self.start_year, is_benchmark=self.is_benchmark)

            self.logger.logger.info("Writing new scenario")
            self.insert_scenario(s.simulation_id)

            s.simulate_scenario(self.years_to_simulate)

        self.logger.logger.info('finished - time elapsed (s) {}'.format(time.time() - start))

    def insert_scenario(self, simulation_id):
        new_scenario = ScenarioDb(simulation_id=simulation_id, scenario_group_id=self.scenario_group_id)
        self.db_handler.write_entities([new_scenario])
