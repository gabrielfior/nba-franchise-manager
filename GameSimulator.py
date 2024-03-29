from dataclasses import dataclass
from typing import List

import numpy as np
from retry import retry
from scipy import interpolate

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

    def simulate_reg_season(self):
        games = self.db_handler.get_games_by_game_type(self.simulation_id, GameTypes.REGULAR_SEASON)
        game_stats_to_write = []
        players: List[PlayerDb] = self.db_handler.get_all(PlayerDb)
        for game in games:
            all_game_stats = self.simulate_game(game, players)
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

        for home_player in home_players:
            points_scored = self.simulate_points_by_player(home_player)
            home_team_points += points_scored
            all_game_stats.append(self.build_game_stats(game, home_player, points_scored))

        for away_player in away_players:
            points_scored = self.simulate_points_by_player(away_player)
            away_team_points += points_scored
            all_game_stats.append(self.build_game_stats(game, home_player, points_scored))

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
        Based on the notebook "analysis_points_scored_per_game", we define an interpolation for deriving the
        stdev of a gaussian centered around the player's scoring average.
        :param points_per_game:
        :return:
        """
        x_points = [3, 10., 30]
        y_points = [1., 0.5, 0.3]

        f2 = interpolate.interp1d(x_points, y_points, kind='linear', fill_value='extrapolate')
        return points_per_game, float(f2(points_per_game)) * points_per_game
