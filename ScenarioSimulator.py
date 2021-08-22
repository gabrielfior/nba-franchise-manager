import uuid
from dataclasses import dataclass

from DraftSimulator import DraftSimulator


@dataclass
class ScenarioSimulator:
    draft_simulator: DraftSimulator

    def __post_init__(self):
        self.simulation_id = str(uuid.uuid4())

    def simulate_scenario(self, n_years):
        for year in range(n_years):
            self.simulate_year()

    def simulate_year(self):
        # simulate draft
        self.draft_simulator.simulate_draft(self.simulation_id)

        # simulate trades
        # simulate season
        # create reports


