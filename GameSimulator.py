from dataclasses import dataclass

import numpy as np

from db.DBHandler import DBHandler
from db.models.game import Game


@dataclass
class GameSimulator:
    simulation_id: str
    db_handler: DBHandler

    def get_games(self):
        return self.db_handler.get_games(self.simulation_id)

    def simulate(self):
        games = self.get_games()
        for game in games:
            self.simulate_game(game)
        self.db_handler.update_games(games)

    def simulate_game(self, game: Game):
        # We will extend this implementation in the future. For now, we randomly assign a winner.
        home_team_points, away_team_points = np.random.choice(list(range(0, 100)), 2, replace=False)
        game.away_team_points = int(away_team_points)
        game.home_team_points = int(home_team_points)
