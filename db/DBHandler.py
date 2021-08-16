from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.draft_pick import DraftPick
from db.models.team import Team


class DBHandler:

    def __init__(self):
        self.engine = create_engine('sqlite:///nba_manager.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_draft_picks(self, year=0):
        with self.Session.begin() as session:
            draft_picks = session.query(DraftPick).filter_by(year=year).order_by(DraftPick.id.asc()).all()
            return draft_picks

    def simulate_draft_lottery(self, year):
        # ToDo - Generate draft picks for next year using previous years`s standings.
        pass

    def store_drafted_players(self, draftees: List, year_drafted: int):
        # List[(int, Player, team_id)]
        with self.Session.begin() as session:
            players = []
            for draft_position, player, team_id in draftees:
                players.append(player)

            session.add_all(players)
        print('committed')

    def get_teams(self) -> List[Team]:
        with self.Session.begin() as session:
            draft_picks = session.query(Team).order_by(Team.id.asc()).all()
            session.expunge_all()
        return draft_picks
