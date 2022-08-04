import pathlib
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd
from fastai.learner import load_learner

from Logger import Logger
from RandomNumberGenerator import RandomNumberGenerator
from db.DBHandler import DBHandler
from db.models.game import GameDb
from db.models.game_stats import GameStatsDb
from db.models.player import PlayerDb
from enums import GameTypes

import lib_platform
if not lib_platform.is_platform_linux: pathlib.PosixPath = pathlib.WindowsPath

class GameTiedException(Exception):
    pass


@dataclass
class GameSimulator:
    db_handler: DBHandler
    simulation_id: str
    model_name: str = "model_gs.pt"
    logger = Logger()
    random_number_generator = RandomNumberGenerator()

    def __post_init__(self):
        self._load_learner()

    def simulate_game_type(self, simulation_id, year, game_type=GameTypes.REGULAR_SEASON):
        games = self.db_handler.get_games_by_game_type(self.simulation_id, game_type, year)
        players: List[PlayerDb] = self.db_handler.get_players_for_season(simulation_id, year)

        self.logger.logger.debug("Start DL predict game")
        self.simulate_using_dl(games, players)
        self.logger.logger.debug("Finished DL predict game")
        self.db_handler.write_entities(games)

        self.logger.logger.debug("Finished simulate game type")

    def simulate_using_dl(self, games: List[GameDb], players: List[PlayerDb]):
        stats_df = self.prepare_stats_df(games, players)
        preds = self.generate_preds(stats_df)
        self.consolidate_games(games, preds)

    def build_game_stats(self, game, player, points_scored):
        game_stats = GameStatsDb(game=game, game_id=game.id,
                                 points_scored=points_scored, player_id=player.id)
        return game_stats

    def _load_learner(self):
        curr_dir = pathlib.PosixPath(__file__).parent.resolve()
        self.learner = load_learner(curr_dir.joinpath('models', self.model_name))  # './models/model_gs.pt')

    def prepare_stats_df(self, games: List[GameDb], players: List[PlayerDb]):
        records = []
        for game in games:
            d = self._prepare_data_single_game(game, players)
            records.append(d)

        return pd.DataFrame(records)

    def _prepare_data_single_game(self, game: GameDb, players: List[PlayerDb]):
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
                d['{team_side}_scorer_{id}'.format(id=idx + 1, team_side=team_side)] = \
                    scorers[idx]
                d['{team_side}_rebounder_{id}'.format(id=idx + 1, team_side=team_side)] = \
                    rebounders[idx]

        return d

    def generate_preds(self, stats_df: pd.DataFrame):

        test_dl = self.learner.dls.test_dl(stats_df)  # Create a test dataloader
        preds, _ = self.learner.get_preds(dl=test_dl, reorder=False)  # Make predictions on it
        return preds

    def consolidate_games(self, games: List[GameDb], preds: List[Tuple]):

        random_numbers = self.random_number_generator.generator.random(len(games))

        for game, prob, random_num in zip(games, preds, random_numbers):

            # We sample from the probability returned by the algo, instead of always picking
            # the most likely outcome.
            home_team_points, away_team_points = 0, 1
            if random_num > prob[0]:
                home_team_points, away_team_points = 1, 0

            game.home_team_points = home_team_points
            game.away_team_points = away_team_points

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
