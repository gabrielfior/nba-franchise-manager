from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.draft_pick import DraftPick
from db.models.game import Game
from db.models.game_mapper import GameMapper
from db.models.team import Team


class DBHandler:

    def __init__(self):
        self.engine = create_engine('sqlite:///nba_manager.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_draft_picks(self, year=0):
        with self.Session.begin() as session:
            draft_picks = session.query(DraftPick).filter_by(year=year).order_by(DraftPick.id.asc()).all()
            session.expunge_all()
            return draft_picks

    def simulate_draft_lottery(self, year):
        # ToDo - Generate draft picks for next year using previous years`s standings.
        pass

    def store_drafted_players(self, draftees: List, year_drafted: int):
        # List[(int, Player, team_id)]
        with self.Session.begin() as session:
            for draft_position, player, team_id in draftees:
                session.add(player)
            session.commit()
        print('committed')

    def get_teams(self) -> List[Team]:
        with self.Session.begin() as session:
            teams = session.query(Team).order_by(Team.id.asc()).all()
            session.expunge_all()
        return teams

    def get_teams_by_team_short_name(self) -> dict:
        with self.Session.begin() as session:
            teams = session.query(Team).order_by(Team.id.asc()).all()
            session.expunge_all()
        teams_by_short_name = {i.short_name: i for i in teams}
        return teams_by_short_name

    def get_game_mappers(self) -> List[GameMapper]:
        with self.Session.begin() as session:
            game_mappers = session.query(GameMapper).all()
            session.expunge_all()
        return game_mappers

    def write_games(self, games: List[Game]):
        with self.Session.begin() as session:
            session.add_all(games)
            session.commit()

    def update_games(self, games):
        with self.Session.begin() as session:
            session.add_all(games)
            session.commit()

    def get_games(self, simulation_id):
        with self.Session.begin() as session:
            game_mappers = session.query(Game).filter(Game.simulation_id == simulation_id).all()
            session.expunge_all()
        return game_mappers
