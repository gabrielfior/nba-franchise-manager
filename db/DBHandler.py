from typing import List

import sqlalchemy
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker, class_mapper

from db.models.draft_pick import DraftPick
from db.models.playoff_bracket import PlayoffBracket as PlayoffBracketDb
from db.models.game import Game
from db.models.game_mapper import GameMapper
from db.models.standing import Standing
from db.models.team import Team
from enums import GameTypes


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

    def get_all(self, cls, filters: List[tuple] = [], order_by: List[tuple] = []) -> List[object]:
        with self.Session.begin() as session:
            table_class = class_mapper(cls)
            filter_statements = []
            for col_name, value in filters:
                filter_statements.append(table_class.c[col_name] == value)
            order_by_statements = []
            for col_name, asc_or_desc in order_by:
                col = table_class.c[col_name]
                sort = asc(col) if asc_or_desc.lower() == 'asc' else desc(col)
                order_by_statements.append(sort)
            # entities = session.query(table_class).all()
            entities = session.query(table_class).where(and_(*filter_statements)).order_by(*order_by_statements).all()
            session.expunge_all()
        return entities

    def get_teams_by_team_short_name(self) -> dict:
        teams_by_short_name = self._get_teams_by_func(lambda x: (x.short_name, x))
        return teams_by_short_name

    def get_teams_by_team_id(self) -> dict:
        teams_by_short_name = self._get_teams_by_func(lambda x: (x.id, x))
        return teams_by_short_name

    def _get_teams_by_func(self, func):
        with self.Session.begin() as session:
            teams = session.query(Team).order_by(Team.id.asc()).all()
            session.expunge_all()
        teams_by_func = {func(i)[0]: func(i)[1] for i in teams}
        return teams_by_func

    def get_game_mappers(self) -> List[GameMapper]:
        with self.Session.begin() as session:
            game_mappers = session.query(GameMapper).all()
            session.expunge_all()
        return game_mappers

    def write_games(self, games: List[Game]):
        with self.Session.begin() as session:
            session.add_all(games)
            session.commit()

    def get_games(self, simulation_id):
        with self.Session.begin() as session:
            game_mappers = session.query(Game).filter(Game.simulation_id == simulation_id).all()
            session.expunge_all()
        return game_mappers

    def get_games_by_game_type(self, simulation_id, game_type: GameTypes):
        with self.Session.begin() as session:
            games = session.query(Game).filter(sqlalchemy.and_(Game.simulation_id == simulation_id,
                                                               Game.game_type == game_type.value)).all()
            session.expunge_all()
        return games

    def write_standings(self, standings):
        with self.Session.begin() as session:
            session.add_all(standings)
            session.commit()

    def delete_games(self, games: Game):
        with self.Session.begin() as session:
            for g in games:
                session.delete(g)
            session.commit()

    def get_standings_by_simulation_id(self, simulation_id):
        return self.get_all(Standing, [('simulation_id',simulation_id)],[('conference', 'asc'), ('position', 'asc')])

    def write_playoff_bracket(self, bracket: PlayoffBracketDb):
        with self.Session.begin() as session:
            session.add(bracket)
            session.commit()