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
from enums import PlayerStatus


def get_local_file_path(filename):
    location = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(location, filename)


def read_initial_data() -> dict:
    filename = 'initial_data.json'
    with open(get_local_file_path(filename), 'r') as x:
        d = json.load(x)
    return d

def read_vegas_odds():
    # ToDo
    pass


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

def read_initial_csv() -> pd.DataFrame:
    return pd.read_csv(get_local_file_path('players_2016_until_2022.csv'))

def read_draft_picks_scoring() -> pd.DataFrame:
    return pd.read_csv(get_local_file_path('scoring_by_pick_number.csv'), header=[0,1], index_col=0)

def get_players(team_dict, players_df: pd.DataFrame) -> List[PlayerDb]:
    players = []
    for player_tuple in players_df.itertuples():
        team_db = team_dict[player_tuple.full_name_team]
        year_drafted = int(player_tuple.SEASON_ID[:4])
        p = PlayerDb(year_drafted=year_drafted,
                     name=player_tuple.full_name_player,
                     points_per_game=player_tuple.PTS_PER_GAME,
                     rebounds_per_game=player_tuple.REB_PER_GAME,
                     assists_per_game=player_tuple.AST_PER_GAME,
                     age=player_tuple.PLAYER_AGE,
                     team=team_db,
                     team_id=team_db.id,
                     simulation_id=None,
                     status=PlayerStatus.EXISTING.value)
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

