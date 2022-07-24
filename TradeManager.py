import itertools
from dataclasses import dataclass
from typing import List

import numpy as np

from Logger import Logger
from db.DBHandler import DBHandler
from db.models.player import PlayerDb


@dataclass
class TradeWrapper:
    from_player_ids: List[int]
    from_ppg: int
    from_team_id: int
    to_player_ids: List[int]
    to_ppg: int
    to_team_id: int


@dataclass
class TradeManager():
    db_handler: DBHandler
    simulation_id: str
    year: int
    logger = Logger()
    tolerance: int = 3
    chance_of_trade_being_executed: float = 0.5
    tolerance_ppg: int = 3
    trades_per_team: int = 1

    def __post_init__(self):
        self.players: List[PlayerDb] = self.db_handler.get_players_for_season(self.simulation_id, self.year)
        self.players_dict = {i.id: i for i in self.players}
        self.teams_dict = self.db_handler.get_teams_by_team_id()

    def execute_trades(self):
        # determine two lists of team_ids. Shuffle.
        teams_ids = list(self.db_handler.get_teams_by_team_id().keys())
        np.random.shuffle(teams_ids)
        mid = int(len(teams_ids) / 2)
        from_team_ids, to_team_ids = teams_ids[:mid], teams_ids[mid:]
        # for each comb of two teams, determine combinations that work.
        for from_team_id, to_team_id in zip(from_team_ids, to_team_ids):
            if np.random.random() > self.chance_of_trade_being_executed:
                # chance of trade not being completed
                continue

            # only 1 trade per team
            trades = self.get_valid_combinations(from_team_id, to_team_id)
            self.store_trades(trades)

    def get_valid_combinations(self, from_team_id, to_team_id):
        from_team_player_ids = [i.id for i in self.players if i.team_id == from_team_id]
        to_team_player_ids = [i.id for i in self.players if i.team_id == to_team_id]
        from_team__combs = self.get_player_sets(from_team_player_ids)
        to_team__combs = self.get_player_sets(to_team_player_ids)
        trades = []
        for comb1, comb2 in zip(from_team__combs, to_team__combs):
            from_player_ids, from_ppg = comb1
            to_player_ids, to_ppg = comb2
            if abs(to_ppg - from_ppg) <= self.tolerance_ppg:
                t = TradeWrapper(from_player_ids=from_player_ids,
                                 from_ppg=from_ppg,
                                 from_team_id=from_team_id,
                                 to_player_ids=to_player_ids,
                                 to_ppg=to_ppg,
                                 to_team_id=to_team_id)
                trades.append(t)

        np.random.shuffle(trades)
        return trades

    def get_player_sets(self, player_ids):
        """
        We get all player combs with lengths [1,2,3].
        :param player_ids:
        :return:
        """
        combs = []
        # for i in range(1, len(player_ids)+1):
        for i in range(1, 4):
            comb = [list(i) for i in itertools.combinations(player_ids, i)]
            for j in comb:
                ppg = self.get_ppg_from_set(j)
                combs.append((j, ppg))
        return combs

    def get_ppg_from_set(self, player_ids):
        ppg = 0
        player_ids = list(player_ids)
        for player_id in player_ids:
            ppg += self.players_dict[player_id].points_per_game
        return ppg

    def store_trades(self, trades: List[TradeWrapper]):
        for trade in trades[:self.trades_per_team]:
            # get players
            # update team_id
            self.db_handler.update_player_team(trade.from_team_id, trade.from_player_ids,
                                               trade.to_team_id, trade.to_player_ids, self.teams_dict)
