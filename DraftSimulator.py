import uuid
from dataclasses import dataclass, field
from typing import List

import numpy as np
from faker import Faker

from db.DBHandler import DBHandler
from db.models.models import DraftPickDb
from db.models.player import PlayerDb

"""
Class for simulating draft in a given year.
"""


@dataclass
class DraftSimulator:
    db_handler: DBHandler
    draft_year: int
    simulation_id: str
    draft_order: List[DraftPickDb] = field(default_factory=list)
    draft_result: List = field(default_factory=list)
    fake = Faker()

    def __post_init__(self):
        self.draft_order = self.db_handler.get_draft_picks(self.draft_year)

    def simulate_draft(self):
        self.model_draft()
        # get standings from previous years (build draft order)
        # also allow for a previous draft order to be given (e.g. for first year)
        # simulate players being taken, return #draft player 1 - id X
        # these draft players will be given performance attributes afterwards, drawn
        # from a distribution of previous draft picks.
        self.store_drafted_players()

    def model_draft(self):
        # returns 60 players with given attributes, determined solely by draft position.
        if not self.draft_order:
            raise Exception('No draft picks could be retrieved, maybe run_initial_data was not started.')
        for draft_position, draft_pick in enumerate(self.draft_order):
            player = self.model_player(draft_pick)
            self.draft_result.append((draft_position, player, draft_pick.team_id))

    def model_player(self, draft_pick: DraftPickDb) -> PlayerDb:
        # ToDo - Generate player`s statistics from draft_position using a distribution of 5 years players
        #  statistics stored in DB.
        points_per_game = np.random.randint(0,2000)/100
        rebounds_per_game = np.random.randint(0,2000)/100
        assists_per_game = np.random.randint(0,2000)/100
        return PlayerDb(name='{} {}'.format(self.fake.first_name_male(), self.fake.last_name()),
                        points_per_game=points_per_game,
                        rebounds_per_game=rebounds_per_game,
                        assists_per_game=assists_per_game,
                        year_drafted=self.draft_year,
                        team=draft_pick.team, team_id=draft_pick.team_id,
                        simulation_id=self.simulation_id)

    def store_drafted_players(self):
        self.db_handler.store_drafted_players(self.draft_result, self.draft_year)