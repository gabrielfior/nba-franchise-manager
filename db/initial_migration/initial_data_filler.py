from db.DBHandler import DBHandler
from db.initial_migration.alembic_helpers import *

from db.models.game import GameDb
from db.models.draft_pick_stats import DraftPickStatsDb
from db.models.models import mapper_registry

class InitialDataFiller:

    def __init__(self, draft_year, db_handler: DBHandler):
        self.draft_year = draft_year
        self.db_handler = db_handler

    def insert_initial_data(self):
        input_data = read_initial_data()
        team_dict = get_team_names(input_data)
        players_df = read_initial_csv()
        draft_picks_stats = read_draft_picks_scoring()
        draft_pick_stats_db = self.create_draft_pick_stats(draft_picks_stats)
        players = get_players(team_dict, players_df)
        draft_picks = get_draft_picks(input_data, team_dict, self.draft_year, simulation_id=None)

        # game_mapper
        game_mappings = get_game_mappings()

        with self.db_handler.Session() as session:
            session.add_all(team_dict.values())
            session.add_all(players)
            session.add_all(draft_picks)
            session.add_all(game_mappings)
            session.add_all(draft_pick_stats_db)

            session.commit()

    def delete_initial_data(self):
        with self.db_handler.Session() as session:
            tablenames = [i.mapper.class_.__tablename__ for i in list(mapper_registry.mappers)]
            for tablename in tablenames:
                session.execute('DELETE from {} where 1=1'.format(tablename))
            session.commit()

    def create_draft_pick_stats(self, draft_picks_stats: pd.DataFrame) -> DraftPickStatsDb:
        l = []
        for pick_number, stats in draft_picks_stats.iterrows():
            for year in range(1, 6):
                points_per_game_mean = stats[f'year{year}_points']['mean']
                points_per_game_std = stats[f'year{year}_points']['std']

                rebounds_per_game_mean = stats[f'year{year}_rebounds']['mean']
                rebounds_per_game_std = stats[f'year{year}_rebounds']['std']

                assists_per_game_mean = stats[f'year{year}_assists']['mean']
                assists_per_game_std = stats[f'year{year}_assists']['std']

                db = DraftPickStatsDb(pick_number=pick_number,
                                      year=year,
                                      points_per_game_mean=points_per_game_mean,
                                      points_per_game_std=points_per_game_std,
                                      rebounds_per_game_mean=rebounds_per_game_mean,
                                      rebounds_per_game_std=rebounds_per_game_std,
                                      assists_per_game_mean=assists_per_game_mean,
                                      assists_per_game_std=assists_per_game_std)
                l.append(db)
        return l