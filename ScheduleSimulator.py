import dataclasses
from dataclasses import dataclass
from datetime import date, datetime

from db.DBHandler import DBHandler
from db.models.game import GameDb
from enums import GameTypes
from helpers import random_date


@dataclass
class ScheduleSimulator:
    db_handler: DBHandler
    year: int
    simulation_id: str
    begin_of_regular_season: datetime = dataclasses.field(init=False) #date(year, 11, 1)
    end_of_regular_season: datetime = dataclasses.field(init=False) #date(year+1, 4, 1)
    game_type: str = GameTypes.REGULAR_SEASON.value

    def __post_init__(self):
        self.begin_of_regular_season = date(self.year, 11, 1)
        self.end_of_regular_season = date(self.year+1, 4, 1)

    def get_random_game_date(self):
        return random_date(self.begin_of_regular_season, self.end_of_regular_season)

    def generate_schedule(self) -> None:
        # read teams from DB
        team_maps = self.db_handler.get_teams_by_team_short_name()
        game_mappers = self.db_handler.get_game_mappers()
        games = []  # tuple - (home_team_id, away_team_id, game_category)

        for game_mapper in game_mappers:
            home_team = team_maps[game_mapper.home_team_short_name]
            away_team = team_maps[game_mapper.away_team_short_name]
            game = GameDb(year=self.year, home_team=home_team, home_team_id=home_team.id,
                          away_team=away_team, away_team_id=away_team.id,
                          game_date=self.get_random_game_date(), simulation_id=self.simulation_id,
                          game_type=self.game_type)
            games.append(game)

            # otherwise add to 3 games

        self.db_handler.write_games(games)