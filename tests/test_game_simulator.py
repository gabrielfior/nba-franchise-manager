import datetime
from typing import List

import factory
from sqlalchemy.orm import scoped_session, sessionmaker

from db.models.game import GameDb
from db.models.player import PlayerDb
from enums import GameTypes


def test_game(game_simulator, mock_simulation_id):
    """
    Boston is a lot better than Washington, so we write a test for determining how often BOS beats WAS.
    We expect 70 x 30 odds roughly.
    """
    players: List[PlayerDb] = game_simulator.db_handler.get_players_for_season(mock_simulation_id, 2021)
    teams_dict = game_simulator.db_handler.get_teams_by_team_short_name()
    celtics_team = teams_dict['BOS']
    wizards_team = teams_dict['WAS']

    class GameFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = GameDb
            sqlalchemy_session = scoped_session(sessionmaker(bind=game_simulator.db_handler.engine))

        year = 2021
        simulation_id = mock_simulation_id
        game_type = GameTypes.REGULAR_SEASON.value
        home_team_id = wizards_team.id
        home_team = wizards_team
        away_team_id = wizards_team.id
        away_team = celtics_team
        game_date = datetime.datetime.now()

    # Test game between Boston Celtics and Washington Wizards 100 times and count values of winners.
    assert game_simulator is not None
    assert game_simulator.db_handler is not None

    # celtics_players = [i for i in players if i.team_id == celtics_team.id]
    # wizards_players = [i for i in players if i.team_id == wizards_team.id]

    bos_wins = 0
    was_wins = 0
    n_simulations = 500
    for simulation_idx in range(n_simulations):
        mock_game_db = GameFactory()
        game_stats = game_simulator.simulate_game(mock_game_db, players)
        bos_won = 1 if mock_game_db.away_team_points > mock_game_db.home_team_points else 0
        bos_wins += bos_won
        was_won = 1 - bos_won
        was_wins += was_won

    # We expect Boston to win most of the times
    print('bos won {} - {} times, was won {} {} times'.format(bos_wins, bos_wins / n_simulations, was_wins,
                                                              was_wins / n_simulations))
