from sqlalchemy import orm

from db.DBHandler import DBHandler
from db.initial_migration.alembic_helpers import *
from alembic import op

from db.models.game import GameDb


class InitialDataFiller:

    def __init__(self, draft_year, db_handler: DBHandler):
        self.draft_year = draft_year
        self.db_handler = db_handler

    def insert_initial_data(self):
        input_data = read_initial_data()
        team_dict = get_team_names(input_data)
        players = get_players(input_data, team_dict)
        draft_picks = get_draft_picks(input_data, team_dict, self.draft_year, simulation_id=None)

        # game_mapper
        game_mappings = get_game_mappings()

        with self.db_handler.Session() as session:
            session.add_all(team_dict.values())
            session.add_all(players)
            session.add_all(draft_picks)
            session.add_all(game_mappings)

            session.commit()

    def delete_initial_data(self):
        with self.db_handler.Session() as session:
            for table in [PlayerDb, TeamDb, DraftPickDb, GameMapperDb, GameDb]:
                session.query(table).delete()
            session.commit()
