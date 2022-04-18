from typing import List

import binarytree
from binarytree import build, Node

from db.models.game import GameDb
from db.models.playoff_bracket import PlayoffBracketDb
from db.models.standing import StandingDb
from enums import GameTypes, Conferences


class PlayoffBracket:

    def __init__(self, simulation_id: str, year: int, standings: List[StandingDb]):

        self.round_level_lookup = {
            GameTypes.CONF_QUARTER_FINALS: -2,
            GameTypes.CONF_SEMIS: -3,
            GameTypes.CONF_FINALS: -4,
            GameTypes.FINALS: -5,
        }
        self.simulation_id = simulation_id
        self.year = year
        self.root: Node = build(self._get_values_for_build(standings))

    def _get_values_for_build(self, standings: List[StandingDb]):
        values = [0] * 15
        # read from standings
        standings_map = {Conferences.EAST.value: {}, Conferences.WEST.value: {}}
        for s in standings:
            standings_map[s.conference][s.position] = s

        # match 1-8, 2-7 etc
        for conf, standings_for_conf in standings_map.items():
            for position1, position2 in [(1, 8), (2, 7), (3, 6), (4, 5)]:
                values.append(standings_for_conf[position1].team.id)
                values.append(standings_for_conf[position2].team.id)

        return values

    @staticmethod
    def get_topmost_node(root, val):
        curr_node = root
        if curr_node is None:
            return None
        elif curr_node.val == val:
            return curr_node
        return PlayoffBracket.get_topmost_node(curr_node.left, val) or PlayoffBracket.get_topmost_node(curr_node.right,
                                                                                                       val)

    def get_matchups(self, round_identifier: GameTypes):
        level = self.round_level_lookup[round_identifier]
        nodes = self.root.levels[level]
        matchups = []
        for node in nodes:
            team_a, team_b = node.left, node.right
            matchups.append((team_a, team_b))
        return matchups

    def update_bracket(self, round_identifier, games: List[GameDb]):
        matchups = self.get_matchups(round_identifier)
        for team_a_node, team_b_node in matchups:
            team_a_id, team_b_id = team_a_node.value, team_b_node.value
            allowed_teams = [team_a_id, team_b_id]
            # get games sorted by ID
            filtered_games = sorted([g for g in games if (g.home_team_id in allowed_teams)
                                     and (g.away_team_id in allowed_teams)], key=lambda g: g.id)

            wins_dict = {team_a_node.value: 0, team_b_node.value: 0}
            winner = None
            games_to_clean_up = []
            for idx, g in enumerate(filtered_games):
                if wins_dict[team_a_id] == 4:
                    winner = team_a_id
                    games_to_clean_up = filtered_games[idx:]
                    break
                elif wins_dict[team_b_id] == 4:
                    winner = team_b_id
                    games_to_clean_up = filtered_games[idx:]
                    break

                if g.home_team_points > g.away_team_points:
                    wins_dict[g.home_team_id] += 1
                else:
                    wins_dict[g.away_team_id] += 1
            # game 7
            if winner is None:
                winner = team_a_id if wins_dict[team_a_id] > wins_dict[team_b_id] else team_b_id
            # get parent of winner
            winner_node = self.get_topmost_node(self.root, winner)
            parent = binarytree.get_parent(self.root, winner_node)
            # update with winner
            parent.val = winner

        return games_to_clean_up

    def to_db(self, simulation_id) -> PlayoffBracketDb:
        pb_db = PlayoffBracketDb(simulation_id=self.simulation_id,
                                 year=self.year,
                                 nodes_sep_comma=','.join([str(i) for i in self.root.values]))
        return pb_db
