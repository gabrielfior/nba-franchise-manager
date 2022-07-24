from dataclasses import dataclass, field
from typing import List

import numpy as np
from faker import Faker

from db.DBHandler import DBHandler
from db.models.models import DraftPickDb
from db.models.player import PlayerDb
from enums import PlayerStatus
from models.draft_pick_stats import DraftPickStatsDb

"""
Class for simulating draft in a given year.
"""


@dataclass
class DraftSimulator:
    db_handler: DBHandler
    draft_year: int
    simulation_id: str
    draft_order: List[DraftPickDb] = field(default_factory=list)
    players_drafted: List = field(default_factory=list)
    fake = Faker()

    def __post_init__(self):
        self.draft_order = self.db_handler.get_draft_picks(self.draft_year, self.simulation_id)

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

        draft_pick_stats = self.db_handler.get_draft_pick_stats()

        for draft_position, draft_pick in enumerate(self.draft_order):
            players = self.model_player(draft_pick, draft_pick_stats)
            self.players_drafted.extend(players)

    def model_player(self, draft_pick: DraftPickDb, draft_pick_stats: List[DraftPickStatsDb]) -> List[PlayerDb]:
        # ToDo - Generate player`s statistics from draft_position using a distribution of 5 years players
        #  statistics stored in DB.

        players = []
        first_name = self.fake.first_name_male()
        last_name = self.fake.last_name()
        for year_number in range(5):
            # Each player drafted is stored 5 times for him to be considered in all years.
            stats = [i for i in draft_pick_stats if i.pick_number == draft_pick.pick_number and
                     i.year == (year_number + 1)][0]
            points_per_game = max(0, np.random.normal(stats.points_per_game_mean,
                                                      scale=stats.points_per_game_std))
            rebounds_per_game = max(0, np.random.normal(stats.rebounds_per_game_mean,
                                                        scale=stats.rebounds_per_game_std))
            assists_per_game = max(0, np.random.normal(stats.assists_per_game_mean,
                                                       scale=stats.assists_per_game_std))
            p = PlayerDb(name='{} {}'.format(first_name, last_name),
                         points_per_game=points_per_game,
                         rebounds_per_game=rebounds_per_game,
                         assists_per_game=assists_per_game,
                         year_drafted=self.draft_year + year_number,
                         team=draft_pick.team, team_id=draft_pick.team_id,
                         simulation_id=self.simulation_id,
                         age=19 + year_number,
                         status=PlayerStatus.DRAFTED.value)
            players.append(p)
        return players

    def store_drafted_players(self):
        self.db_handler.store_drafted_players(self.players_drafted)
