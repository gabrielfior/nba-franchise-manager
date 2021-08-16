import datetime
from dataclasses import dataclass, field
from typing import List, Tuple

from db.DBHandler import DBHandler


# ToDo - Move to models
# class Game:
#     id: int
#     home_team: Team
#     away_team: Team
#     game_date: datetime.datetime
#
#
# @dataclass
# class GameResult:
#     game: Game
#     winner: Team
#     loser: Team
#
#
# class RegularSeasonSchedule:
#     games: Game
#
#
# class PlayoffSchedule:
#     games: Game
#
#
# @dataclass()
# class Standings:
#     team_positions: List[Tuple[int, Team]]  # teams are sorted according to position.


"""
Class for simulating one 82-game season.
"""


@dataclass
class SeasonSimulator:
    #regular_season_schedule: RegularSeasonSchedule
    #regular_season_standings: Standings
    #playoff_schedule: PlayoffSchedule
    #playoff_standings: Standings
    db_handler: DBHandler

    def __init__(self) -> None:
        self.db_handler = DBHandler()

    def main(self):
        self.simulate_regular_season()
        self.simulate_playoffs()

    def simulate_regular_season(self):
        #self.standings = self.regular_season_schedule.simulate()
        pass

    def simulate_playoffs(self):
        #self.playoff_standings = self.playoff_schedule.simulate()
        pass

    def store_results(self):
        pass
        # store results in DB
        #self.regular_season_standings.store()
        #self.playoff_standings.store()