import csv
import json
from typing import List

from db.models.draft_pick import DraftPick
from db.models.game_mapper import GameMapper
from db.models.player import Player
from db.models.team import Team
import pandas as pd


# revision identifiers, used by Alembic.

def read_initial_data() -> dict:
    # pdb.set_trace()
    filename = './alembic/initial_data.json'
    with open(filename, 'r') as x:
        d = json.load(x)
    return d


def get_team_names(input_data) -> dict:
    teams = input_data['teams']
    return {i['name']: Team(name=i['name'], conference=i['conference'],
                            division=i['division'],
                            short_name=i['shortName']) for i in teams}


def get_team_short_names(input_data) -> dict:
    teams = input_data['teams']
    return {i['shortName']: Team(name=i['name'], conference=i['conference'],
                                 division=i['division'],
                                 short_name=i['shortName']) for i in teams}


def get_players(input_data, team_dict) -> List[Player]:
    teams = input_data['teams']
    players = []
    for team in teams:
        team_db = team_dict[team['name']]
        for player in team['players']:
            p = Player(year_drafted=-1,
                       name=player['name'],
                       points_per_game=player['points_per_game'],
                       rebounds_per_game=player['rebounds_per_game'],
                       assists_per_game=player['assists_per_game'],
                       team=team_db,
                       team_id=team_db.id)
            players.append(p)
    return players


def get_draft_picks(input_data, teams_dict, year) -> List[DraftPick]:
    draft_picks = []
    for pick_number, team_name in enumerate(input_data['draft_positions']):
        draft_pick = DraftPick(team=teams_dict[team_name],
                               pick_number=pick_number,
                               team_id=teams_dict[team_name].id,
                               year=year)
        draft_picks.append(draft_pick)
    return draft_picks


def get_game_mappings():
    from pbpstats.data_loader import DataNbaScheduleLoader
    game_mappers = []
    schedule_loader = DataNbaScheduleLoader("nba", "2018-2019", "Regular Season", "web")

    df = pd.DataFrame([i.data for i in schedule_loader.items])
    for row_index, row_tuple in df.iterrows():
        gm = GameMapper(home_team_short_name=row_tuple['home_team_abbreviation'],
                        away_team_short_name=row_tuple['away_team_abbreviation'])
        game_mappers.append(gm)
    return game_mappers

