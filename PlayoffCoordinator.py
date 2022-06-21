import dataclasses
from datetime import date

from GameSimulator import GameSimulator
from Logger import Logger
from PlayoffBracket import PlayoffBracket
from db.DBHandler import DBHandler
from db.models.game import GameDb
from db.models.team import TeamDb
from enums import GameTypes
from helpers import random_date


@dataclasses.dataclass
class PlayoffCoordinator:
    db_handler: DBHandler
    simulation_id: str
    year: int
    game_simulator: GameSimulator
    logger = Logger()

    def __post_init__(self):
        # self.begin_of_regular_season = date(self.year, 11, 1)
        # self.end_of_regular_season = date(self.year + 1, 4, 1)
        self.playoff_dates = {
            GameTypes.CONF_QUARTER_FINALS: {
                'begin': date(self.year, 4, 10),
                'end': date(self.year, 4, 24),
            },
            GameTypes.CONF_SEMIS: {
                'begin': date(self.year, 4, 27),
                'end': date(self.year, 5, 12),
            },
            GameTypes.CONF_FINALS: {
                'begin': date(self.year, 5, 15),
                'end': date(self.year, 5, 30),
            },
            GameTypes.FINALS: {
                'begin': date(self.year, 6, 1),
                'end': date(self.year, 6, 15),
            }
        }

    def simulate_playoffs(self):

        bracket = self.create_bracket()

        for round_identifier in GameTypes:
            if round_identifier == GameTypes.REGULAR_SEASON:
                continue

            self.create_playoff_games(round_identifier, bracket)
            self.simulate_games(round_identifier)
            self.update_bracket(round_identifier, bracket)

        bracket_db = bracket.to_db(self.simulation_id)
        self.db_handler.write_entities([bracket_db])

    def create_bracket(self) -> PlayoffBracket:
        # read from standings
        standings = self.db_handler.get_standings_by_simulation_id(self.simulation_id)
        self.logger.logger.debug("Retrieved {} standings".format(len(standings)))
        pb = PlayoffBracket(self.simulation_id, self.year, standings)
        return pb

    def create_playoff_games(self, round_identifier: GameTypes, bracket: PlayoffBracket):

        matchups = bracket.get_matchups(round_identifier)
        team_dict = self.db_handler.get_teams_by_team_id()
        for team_a_node, team_b_node in matchups:
            self.generate_games_for_matchup(round_identifier, team_dict[team_a_node.value], team_dict[team_b_node.value])

    def update_bracket(self, round_identifier: GameTypes, bracket: PlayoffBracket):
        games = self.db_handler.get_games_by_game_type(self.simulation_id, round_identifier)

        games_to_clean_up = bracket.update_bracket(round_identifier, games)
        self.db_handler.delete_games(games_to_clean_up)

    def simulate_games(self, round: GameTypes):
        self.game_simulator.simulate_game_type(self.simulation_id, self.year, round)

    def generate_games_for_matchup(self, round_identifier, team_a: TeamDb, team_b: TeamDb):
        # Generate 2-2-1-1-1 games (home vs away)
        games = []
        for game_idx in range(1, 8):
            home_team = team_a if game_idx in [1, 2, 5, 7] else team_b
            away_team = team_b if game_idx in [1, 2, 5, 7] else team_a

            game_date = random_date(self.playoff_dates[round_identifier]['begin'],
                                    self.playoff_dates[round_identifier]['end'])
            game = GameDb(year=self.year, home_team=home_team, home_team_id=home_team.id,
                          away_team=away_team, away_team_id=away_team.id,
                          game_date=game_date, simulation_id=self.simulation_id,
                          game_type=round_identifier.value)
            games.append(game)
        # Write games into DB
        self.db_handler.write_entities(games)
