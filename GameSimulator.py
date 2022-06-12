from dataclasses import dataclass

import numpy as np
from retry import retry
from scipy import interpolate

from db.DBHandler import DBHandler
from db.models.game import GameDb
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
        for game in games:
            self.simulate_game(game)
        self.db_handler.write_entities(games)

    def simulate_game(self, game: GameDb):
        """
        We simulate a game by summing up the points scored by each player. If the final score remains tied, we restart
        the simulation until a valid final score has been reached, which is a scenario in which team A has more points than
        team B.
        :param game:
        :return:
        """

        home_team_points, away_team_points = self.simulate_total_points_in_game(game)

        game.away_team_points = int(away_team_points)
        game.home_team_points = int(home_team_points)

    @retry(GameTiedException, tries=5)
    def simulate_total_points_in_game(self, game):
        home_team_points = 0
        away_team_points = 0

        home_players = self.db_handler.get_players_by_team(game.home_team.id)
        away_players = self.db_handler.get_players_by_team(game.away_team.id)

        for home_player in home_players:
            home_team_points += self.simulate_points_by_player(home_player)

        for away_player in away_players:
            away_team_points += self.simulate_points_by_player(away_player)

        if home_team_points == away_team_points:
            raise GameTiedException()

        return home_team_points, away_team_points

    def simulate_points_by_player(self, player: PlayerDb) -> int:
        mu, sigma = self.make_distribution_for_player(player.points_per_game)
        z = np.random.normal(mu, sigma, 1)
        return int(np.rint(z))

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
        return points_per_game, float(f2(points_per_game))*points_per_game
