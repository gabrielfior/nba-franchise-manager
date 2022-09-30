import datetime

import factory
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from db.models.game import GameDb
from db.models.player import PlayerDb
from enums import GameTypes


@pytest.mark.parametrize("team_home_short_name,team_away_short_name", [("BOS", "OKC"), ("OKC", "BOS"),
                                                                       ("DET", "PHX"), ("NYK", "GSW"),
                                                                       ])
def test_game_combinations(team_home_short_name, team_away_short_name, game_simulator, mock_simulation_id):
    """
    Boston is a lot better than OKC, so we write a test for determining how often BOS beats OKC.
    We expect 75 x 25 odds roughly.
    """
    run_game(team_home_short_name, team_away_short_name, game_simulator, mock_simulation_id)

def run_game(team_home_short_name, team_away_short_name, game_simulator, mock_simulation_id):
    players: dict[int, PlayerDb] = {p.id: p for p in
                                    game_simulator.db_handler.get_players_for_season(mock_simulation_id, 2021)}
    teams_dict = game_simulator.db_handler.get_teams_by_team_short_name()
    team_home = teams_dict[team_home_short_name]
    team_away = teams_dict[team_away_short_name]

    class GameFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = GameDb
            sqlalchemy_session = scoped_session(sessionmaker(bind=game_simulator.db_handler.engine))

        year = 2021
        simulation_id = mock_simulation_id
        game_type = GameTypes.REGULAR_SEASON.value
        home_team_id = team_home.id
        home_team = team_home
        away_team_id = team_away.id
        away_team = team_away
        game_date = datetime.datetime.now()

    home_wins = 0
    away_wins = 0
    n_simulations = 100
    for simulation_idx in range(n_simulations):
        mock_game_db = GameFactory()
        game_simulator.simulate_using_team_stats([mock_game_db], list(players.values()))
        home_win = 0 if mock_game_db.away_team_points > mock_game_db.home_team_points else 1
        away_win = 1 if mock_game_db.away_team_points > mock_game_db.home_team_points else 0

        home_wins += home_win
        away_wins += away_win

        # We expect Boston to win most of the times
    print(f'{team_home_short_name} won {home_wins} - {home_wins / n_simulations} times,'
          f' {team_away_short_name} won {away_wins} {away_wins / n_simulations} times')
