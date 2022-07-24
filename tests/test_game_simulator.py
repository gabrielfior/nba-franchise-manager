import datetime
from sqlalchemy import MetaData
import factory
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from db.models.game import GameDb
from db.models.player import PlayerDb
from enums import GameTypes

# Leave it here for importing classes


def test_game(game_simulator, mock_simulation_id):
    """
    Boston is a lot better than OKC, so we write a test for determining how often BOS beats OKC.
    We expect 75 x 25 odds roughly.
    """
    players: dict[int, PlayerDb] = {p.id: p for p in
                                    game_simulator.db_handler.get_players_for_season(mock_simulation_id, 2021)}
    teams_dict = game_simulator.db_handler.get_teams_by_team_short_name()
    celtics_team = teams_dict['BOS']
    okc_team = teams_dict['OKC']

    class GameFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = GameDb
            sqlalchemy_session = scoped_session(sessionmaker(bind=game_simulator.db_handler.engine))

        year = 2021
        simulation_id = mock_simulation_id
        game_type = GameTypes.REGULAR_SEASON.value
        home_team_id = okc_team.id
        home_team = okc_team
        away_team_id = celtics_team.id
        away_team = celtics_team
        game_date = datetime.datetime.now()

    bos_wins = 0
    okc_wins = 0
    n_simulations = 100
    for simulation_idx in range(n_simulations):
        mock_game_db = GameFactory()
        #game_stats = game_simulator.simulate_game(mock_game_db, list(players.values()))
        game_stats = game_simulator.simulate_game_using_dl(mock_game_db, list(players.values()))
        sorted_game_stats = dict(sorted({players[g.player_id].name: g.points_scored for g in game_stats}.items(), key=lambda x: x[1], reverse=True))
        for k, v in players.items():
            if k in sorted_game_stats:
                sorted_game_stats[k].player = v
        bos_won = 1 if mock_game_db.away_team_points > mock_game_db.home_team_points else 0
        bos_wins += bos_won
        okc_won = 1 - bos_won
        okc_wins += okc_won

    print(sorted_game_stats)

    # We expect Boston to win most of the times
    print('bos won {} - {} times, okc won {} {} times'.format(bos_wins, bos_wins / n_simulations, okc_wins,
                                                              okc_wins / n_simulations))
