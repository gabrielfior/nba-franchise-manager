from dataclasses import dataclass

from db.DBHandler import DBHandler

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