from dataclasses import dataclass

import numpy as np

from db.DBHandler import DBHandler
from db.models.game import Game
from enums import GameTypes


@dataclass
class GameSimulator:
    simulation_id: str
    db_handler: DBHandler

    def simulate_reg_season(self):
        games = self.db_handler.get_games_by_game_type(self.simulation_id, GameTypes.REGULAR_SEASON)
        for game in games:
            self.simulate_game(game)
        self.db_handler.write_games(games)

    def simulate_game(self, game: Game):
        # We will extend this implementation in the future. For now, we randomly assign a winner.
        home_team_points, away_team_points = np.random.choice(list(range(0, 100)), 2, replace=False)
        game.away_team_points = int(away_team_points)
        game.home_team_points = int(home_team_points)
