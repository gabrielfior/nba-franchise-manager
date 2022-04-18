import json
import os
from typing import List
import pathlib
import pandas as pd
from pbpstats.data_loader import DataNbaScheduleWebLoader, DataNbaScheduleLoader

from db.models.draft_pick import DraftPickDb
from db.models.game_mapper import GameMapperDb
from db.models.player import PlayerDb
from db.models.team import TeamDb


# revision identifiers, used by Alembic.

def read_initial_data() -> dict:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = 'initial_data.json'
    with open(os.path.join(__location__, filename), 'r') as x:
        d = json.load(x)
    return d


def get_team_names(input_data) -> dict:
    teams = input_data['teams']
    return {i['name']: TeamDb(name=i['name'], conference=i['conference'],
                              division=i['division'],
                              short_name=i['shortName']) for i in teams}


def get_team_short_names(input_data) -> dict:
    teams = input_data['teams']
    return {i['shortName']: TeamDb(name=i['name'], conference=i['conference'],
                                   division=i['division'],
                                   short_name=i['shortName']) for i in teams}


def get_players(input_data, team_dict) -> List[PlayerDb]:
    teams = input_data['teams']
    players = []
    for team in teams:
        team_db = team_dict[team['name']]
        for player in team['players']:
            p = PlayerDb(year_drafted=-1,
                         name=player['name'],
                         points_per_game=player['points_per_game'],
                         rebounds_per_game=player['rebounds_per_game'],
                         assists_per_game=player['assists_per_game'],
                         team=team_db,
                         team_id=team_db.id,
                         simulation_id=None)
            players.append(p)
    return players


def get_draft_picks(input_data, teams_dict, year, simulation_id) -> List[DraftPickDb]:
    draft_picks = []
    for pick_number, team_name in enumerate(input_data['draft_positions']):
        draft_pick = DraftPickDb(team=teams_dict[team_name],
                                 pick_number=pick_number+1,
                                 team_id=teams_dict[team_name].id,
                                 year=year,
                                 simulation_id=simulation_id)
        draft_picks.append(draft_pick)
    return draft_picks


def get_game_mappings():
    game_mappers = []
    current_dir = pathlib.Path(__file__).parent
    w = DataNbaScheduleWebLoader(current_dir.joinpath('pbpstats_data'))
    schedule_loader = DataNbaScheduleLoader("nba", "2018-2019", "Regular Season", w)

    df = pd.DataFrame([i.data for i in schedule_loader.items])
    for row_index, row_tuple in df.iterrows():
        gm = GameMapperDb(home_team_short_name=row_tuple['home_team_abbreviation'],
                          away_team_short_name=row_tuple['away_team_abbreviation'])
        game_mappers.append(gm)
    return game_mappers

