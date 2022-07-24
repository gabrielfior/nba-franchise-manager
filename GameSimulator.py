import pathlib
from dataclasses import dataclass
from typing import List
from alive_progress import alive_it

import numpy as np
import pandas as pd
from alive_progress import alive_bar
from fastai.learner import load_learner
from retry import retry

from db.DBHandler import DBHandler
from db.models.game import GameDb
from db.models.game_stats import GameStatsDb
from db.models.player import PlayerDb
from enums import GameTypes


class GameTiedException(Exception):
    pass


@dataclass
class GameSimulator:
    db_handler: DBHandler
    simulation_id: str
    model_name: str = "model_gs.pt"

    def __post_init__(self):
        self._load_learner()

    def simulate_game_type(self, simulation_id, year, game_type=GameTypes.REGULAR_SEASON):
        games = self.db_handler.get_games_by_game_type(self.simulation_id, game_type, year)
        players: List[PlayerDb] = self.db_handler.get_players_for_season(simulation_id, year)
        game_stats_to_write = []

        for game in games:
            all_game_stats = self.simulate_game_using_dl(game, players)
            game_stats_to_write.extend(all_game_stats)
        self.db_handler.write_entities(games)
        self.db_handler.write_entities(game_stats_to_write)

    def simulate_game(self, game: GameDb, players: List[PlayerDb]) -> List[GameStatsDb]:
        """
        We simulate a game by summing up the points scored by each player. If the final score remains tied, we restart
        the simulation until a valid final score has been reached, which is a scenario in which team A has more points than
        team B.
        :param game:
        :return:
        """

        home_players = [i for i in players if i.team_id == game.home_team_id]
        away_players = [i for i in players if i.team_id == game.away_team_id]

        home_team_points, away_team_points, all_game_stats = self.simulate_total_points_in_game(game, home_players,
                                                                                                away_players)
        game.away_team_points = int(away_team_points)
        game.home_team_points = int(home_team_points)

        return all_game_stats

    @retry(GameTiedException, tries=5)
    def simulate_total_points_in_game(self, game, home_players, away_players) -> List[GameStatsDb]:
        home_team_points = 0
        away_team_points = 0
        all_game_stats = []

        # Also check https://github.com/PlayingNumbers/NBASimulator/blob/master/NBAFinalsSimulation.ipynb
        # for simulating games

        if len(home_players) == 0 or len(away_players) == 0:
            raise Exception("No players found for team.\n Home players - {} \n Away players - {}".format(home_players,
                                                                                                         away_players))

        for home_player in home_players:
            points_scored = self.simulate_points_by_player(home_player)
            home_team_points += points_scored
            all_game_stats.append(self.build_game_stats(game, home_player, points_scored))

        for away_player in away_players:
            points_scored = self.simulate_points_by_player(away_player)
            away_team_points += points_scored
            all_game_stats.append(self.build_game_stats(game, away_player, points_scored))

        if home_team_points == away_team_points:
            raise GameTiedException()

        return home_team_points, away_team_points, all_game_stats

    def build_game_stats(self, game, player, points_scored):
        game_stats = GameStatsDb(game=game, game_id=game.id,
                                 points_scored=points_scored, player_id=player.id)
        return game_stats

    def simulate_points_by_player(self, player: PlayerDb) -> int:
        mu, sigma = self.make_distribution_for_player(player.points_per_game)
        z = np.random.normal(mu, sigma, 1)
        return max(0, int(np.rint(z)))

    def make_distribution_for_player(self, points_per_game: float) -> float:
        """
        Based on the notebook "analysis_points_scored_per_game", we define a linear regression function for deriving
        the stdev of a gaussian centered around the player's scoring average.
        :param points_per_game:
        :return:
        """
        intercept = 2.524495
        coef = 0.26738

        std_dev = points_per_game * coef + intercept
        return points_per_game, std_dev

    def _load_learner(self):
        curr_dir = pathlib.Path(__file__).parent.resolve()
        self.learner = load_learner(curr_dir.joinpath('models', self.model_name))  # './models/model_gs.pt')

    def simulate_game_using_dl(self, game: GameDb, players: List[PlayerDb]):

        home_players = [i for i in players if i.team_id == game.home_team_id]
        away_players = [i for i in players if i.team_id == game.away_team_id]

        home_scorers_points = self.get_top_n_scorers_from_team(home_players, 5)
        home_scorers_rebounders = self.get_top_n_rebounders_from_team(home_players, 5)

        away_scorers_points = self.get_top_n_scorers_from_team(away_players, 5)
        away_scorers_rebounders = self.get_top_n_rebounders_from_team(away_players, 5)

        if len(home_scorers_points) != len(away_scorers_points):
            raise Exception('len home scorers {} != len away scorers {}'.format(
                len(home_scorers_points), len(away_scorers_points)))

        d = {}
        for idx in range(len(home_scorers_points)):
            for team_side, scorers, rebounders in zip(
                    ['home', 'away'],
                    [home_scorers_points, away_scorers_points],
                    [home_scorers_rebounders, away_scorers_rebounders]):
                # for metric in ['scorer', 'rebounder']:
                d['{team_side}_scorer_{id}'.format(id=idx+1, team_side=team_side)] = \
                    scorers[idx]
                d['{team_side}_rebounder_{id}'.format(id=idx+1, team_side=team_side)] = \
                    rebounders[idx]

        row, clas, probs = self.learner.predict(pd.Series(d))
        random_num = np.random.random() # [0,1]

        # We sample from the probability returned by the algo, instead of always picking
        # the most likely outcome.
        home_won = 0
        if random_num > probs[0]:
            home_won = 1

        if home_won == 1:
            home_team_points, away_team_points = 1, 0
        else:
            home_team_points, away_team_points = 0, 1

        game.home_team_points = home_team_points
        game.away_team_points = away_team_points

        return []

    def get_top_n_scorers_from_team(self, players, n=3):
        return self._get_in_sorted_order(players, 'points_per_game', n)

    def get_top_n_rebounders_from_team(self, players, n=3):
        return self._get_in_sorted_order(players, 'rebounds_per_game', n)

    def _get_in_sorted_order(self, players, col_name, n):
        sorted_players = sorted(players, key=lambda x: x.__getattribute__(col_name), reverse=True)
        top_n_players = [i.__getattribute__(col_name) for i in sorted_players[:n]]
        if len(sorted_players) < n:
            top_n_players += [0] * (n - len(players))

        return top_n_players
