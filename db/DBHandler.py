import os
from typing import List, Dict

import sqlalchemy
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker, class_mapper

from db.models.draft_pick import DraftPickDb
from db.models.draft_pick_stats import DraftPickStatsDb
from db.models.game import GameDb
from db.models.game_mapper import GameMapperDb
from db.models.player import PlayerDb
from db.models.standing import StandingDb
from db.models.team import TeamDb
from enums import GameTypes, PlayerStatus
from dotenv import load_dotenv
load_dotenv()

class DBHandler:

    def __init__(self, engine=None, echo=False):
        if engine is None:
            db_url = os.environ.get('AWS_DB_URL')
            if db_url is None:
                raise Exception('AWS_DB_URL not defined')
            self.engine = create_engine(db_url, echo=echo)
        else:
            self.engine = engine

        self.Session = sessionmaker(bind=self.engine)

    def get_draft_picks(self, year, simulation_id):
        with self.Session.begin() as session:
            entities = session.query(DraftPickDb).filter(
                and_(DraftPickDb.year == year,
                     DraftPickDb.simulation_id == simulation_id,
                     )).order_by(DraftPickDb.id.asc()).all()

            session.expunge_all()
            if (len(entities) != 60):
                raise Exception('Expected 60 draft picks')
            return entities

    def store_drafted_players(self, players_drafted: List[PlayerDb]):
        with self.Session.begin() as session:
            for player in players_drafted:
                session.add(player)
            session.commit()

    def get_teams(self) -> List[TeamDb]:
        with self.Session.begin() as session:
            teams = session.query(TeamDb).order_by(TeamDb.id.asc()).all()
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
            teams = session.query(TeamDb).order_by(TeamDb.id.asc()).all()
            session.expunge_all()
        teams_by_func = {func(i)[0]: func(i)[1] for i in teams}
        return teams_by_func

    def get_game_mappers(self) -> List[GameMapperDb]:
        with self.Session.begin() as session:
            game_mappers = session.query(GameMapperDb).all()
            session.expunge_all()
        return game_mappers

    def get_games(self, simulation_id):
        with self.Session.begin() as session:
            game_mappers = session.query(GameDb).filter(GameDb.simulation_id == simulation_id).all()
            session.expunge_all()
        return game_mappers

    def get_games_by_game_type(self, simulation_id, game_type: GameTypes, year: int):
        with self.Session.begin() as session:
            games = session.query(GameDb).filter(sqlalchemy.and_(GameDb.simulation_id == simulation_id,
                                                                 GameDb.year == year,
                                                                 GameDb.game_type == game_type.value)).all()
            session.expunge_all()
        return games

    def write_entities(self, entities):
        with self.Session.begin() as session:
            # session.add_all(entities)
            session.bulk_save_objects(entities)
            session.commit()

    def delete_games(self, games: GameDb):
        with self.Session.begin() as session:
            for g in games:
                session.delete(g)
            session.commit()

    def get_standings_by_simulation_id_and_year(self, simulation_id: str, year: int):
        return self.get_all(StandingDb,
                            [('simulation_id', simulation_id), ('year', year)],
                            [('conference', 'asc'), ('position', 'asc')])

    def get_players_for_season(self, simulation_id: str, year: int):
        with self.Session.begin() as session:
            # get previous players (simulation_id = None) + newly drafted players (simulation_id == simulation_id)
            entities = session.query(PlayerDb).filter(
                and_(PlayerDb.simulation_id == simulation_id,
                     PlayerDb.year_drafted == year)).all()
            session.expunge_all()
        return entities

    def get_draft_pick_stats(self):
        return self.get_all(DraftPickStatsDb)

    def update_player_team(self, from_team_id: int, from_player_ids: List[int],
                           to_team_id: int, to_player_ids: List[int], team_id_dict: Dict):
        with self.Session.begin() as session:
            # from team
            session.query(PlayerDb).filter(PlayerDb.id.in_(from_player_ids)).update(
                {'team_id': from_team_id, 'status': PlayerStatus.TRADED.value})
            # to team
            session.query(PlayerDb).filter(PlayerDb.id.in_(to_player_ids)).update(
                {'team_id': to_team_id, 'status': PlayerStatus.TRADED.value})

            session.commit()
