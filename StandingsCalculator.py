import dataclasses

import numpy as np
import pandas as pd

from db.DBHandler import DBHandler
from db.models.standing import StandingDb
from enums import Conferences


@dataclasses.dataclass
class StandingsCalculator:
    db_handler: DBHandler
    simulation_id: str
    year: int

    def calculate_standings(self):
        self.retrieve_games_and_teams()
        games_df = pd.DataFrame.from_records([dataclasses.asdict(game) for game in self.games])

        games_df['team_won'] = games_df.apply(
            lambda x: x['home_team_id'] if x['home_team_points'] > x['away_team_points'] else \
                x['away_team_id'], axis=1)
        games_df['team_lost'] = games_df.apply(
            lambda x: x['away_team_id'] if x['home_team_points'] > x['away_team_points'] else \
                x['home_team_id'], axis=1)

        ordered_teams = self.calc_ordered_teams(games_df)

        # ToDo - Write standings on each team
        standings = []
        for _, conf_team_ids in ordered_teams.items():
            for conf_position, conf_team_id in enumerate(conf_team_ids):
                team = self.teams_dict[conf_team_id]
                s = StandingDb(simulation_id=self.simulation_id,
                               year=self.year,
                               team=team,
                               team_id=team.id,
                               division=team.division,
                               conference=team.conference,
                               position=conf_position+1
                               )
                standings.append(s)

        self.db_handler.write_standings(standings)

    def calc_ordered_teams(self, games_df):
        ranked_wins = games_df.groupby(by='team_won', as_index=False)['id'].agg('count').sort_values('id',
                                                                                                     ascending=False)
        grouped_standings = ranked_wins.groupby(by='id')['team_won'].apply(list).sort_index(ascending=False)
        ordered_teams = {Conferences.EAST.value: [], Conferences.WEST.value: []}
        for win_total, team_ids in grouped_standings.iteritems():
            np.random.shuffle(team_ids)
            for team_id in team_ids:
                team_item = self.teams_dict[team_id]
                conference = team_item.conference
                ordered_teams[conference].append(team_id)
        return ordered_teams

    def retrieve_games_and_teams(self):
        self.games = self.db_handler.get_games(self.simulation_id)
        self.teams_dict = self.db_handler.get_teams_by_team_id()
