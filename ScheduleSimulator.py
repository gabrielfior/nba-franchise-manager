from collections import defaultdict
from dataclasses import dataclass

from db.DBHandler import DBHandler
from db.models.game_type import GameDescription
from numpy import random
import tabulate


@dataclass
class ScheduleSimulator:
    db_handler: DBHandler

    # ToDo - Move to alembic script

    def ok_to_proceed(self, games_out_of_division_for_team, home_team_id, away_team_id) -> bool:
        should_stop = games_out_of_division_for_team[home_team_id]['3games'].__contains__(away_team_id) or \
                games_out_of_division_for_team[home_team_id]['4games'].__contains__(away_team_id)
        return not should_stop


    def generate_schedule(self) -> None:
        # read teams from DB
        teams = self.db_handler.get_teams()
        game_tuples = []  # tuple - (home_team_id, away_team_id, game_category)

        for home_team in teams:
            for away_team in teams:
                if home_team == away_team:
                    continue
            # create games in_division
            # each team plays each other 4 times - 2
            if home_team.division == away_team.division:
                game_tuple1 = (home_team.id, away_team.id, GameDescription.IN_CONFERENCE_IN_DIVISION)
                game_tuple2 = (away_team.id, home_team.id, GameDescription.IN_CONFERENCE_IN_DIVISION)
                game_tuples.extend([game_tuple1, game_tuple2, game_tuple1, game_tuple2])  # 2 home games, 2 away games
            # add other conference games
            elif home_team.conference != away_team.conference:
                game_tuple1 = (home_team.id, away_team.id, GameDescription.OUT_OF_CONFERENCE)  # 1 home game
                game_tuple2 = (away_team.id, home_team.id, GameDescription.OUT_OF_CONFERENCE)  # 1 away game
                game_tuples.extend([game_tuple1, game_tuple2])

        # out-of-division
        random.shuffle(teams)
        games_out_of_division_for_team = defaultdict(lambda: {'3games': [], '4games': []})  # initializes to 0
        for home_idx, home_team in enumerate(teams):
            for away_team in teams[home_idx+1:]:
                if not self.ok_to_proceed(games_out_of_division_for_team, home_team.id, away_team.id):
                    continue

                # 4 games with first 6 teams
                # 3 games with other 4 teams
                if home_team.division != away_team.division and home_team.conference == away_team.conference:
                    # try to add to 4 games

                    if len(games_out_of_division_for_team[home_team.id]['4games']) < 6 and \
                            len(games_out_of_division_for_team[away_team.id]['4games']) < 6:
                        # avoid duplicate games

                        games_out_of_division_for_team[home_team.id]['4games'].append(away_team.id)
                        games_out_of_division_for_team[away_team.id]['4games'].append(home_team.id)
                        # generate 4 games
                        game_tuple1 = (home_team.id, away_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                        game_tuple2 = (away_team.id, home_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                        game_tuples.extend(
                            [game_tuple1, game_tuple2, game_tuple1, game_tuple2])  # 2 home games, 2 away games

                    elif len(games_out_of_division_for_team[home_team.id]['3games']) < 4 and \
                            len(games_out_of_division_for_team[away_team.id]['3games']) < 4:

                        games_out_of_division_for_team[home_team.id]['3games'].append(away_team.id)
                        games_out_of_division_for_team[away_team.id]['3games'].append(home_team.id)
                        # generate 3 games
                        # if i % 2 ==0, 2x home, else 1x home
                        if len(games_out_of_division_for_team[home_team.id]['3games']) % 2 == 0:
                            # 2x home
                            game_tuple1 = (home_team.id, away_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                            game_tuple2 = (home_team.id, away_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                            game_tuple3 = (away_team.id, home_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                        else:
                            # 1x home
                            game_tuple1 = (home_team.id, away_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                            game_tuple2 = (away_team.id, home_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                            game_tuple3 = (away_team.id, home_team.id, GameDescription.IN_CONFERENCE_OUT_OF_DIVISION)
                        game_tuples.extend(
                            [game_tuple1, game_tuple2, game_tuple1, game_tuple3])  # 2 home games, 2 away games

                    # otherwise add to 3 games
        print(tabulate.tabulate(games_out_of_division_for_team.items()))
        #print(tabulate.tabulate(game_tuples))
        # ToDo - Generate games
        # get random
        # add 4 games out-of-division
        # add 6 games out-of-division
        '''
        # generate all games
            # 4 games (HOME, HOME, AWAY, AWAY) with 4 teams from same division -> total 16 games
            # 2 games (HOME, AWAY) with 15 teams from other conference -> total 30 games
            # With teams outside division (10):
                # get random 4, play 3 games (total 12)
                # get random 6, play 4 games (total 24)
            # this schedule remains fixed - random order becomes consolidated
        #https: // www.wearebasket.net / explain - game - 82 - games - schedule /
        '''
