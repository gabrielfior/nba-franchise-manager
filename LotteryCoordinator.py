import dataclasses

from db.DBHandler import DBHandler
from db.models.draft_pick import DraftPickDb


@dataclasses.dataclass
class LotteryCoordinator:
    db_handler: DBHandler
    simulation_id: str
    year: int

    def generate_lottery(self):
        """
        For simplicity reasons, we simply generate draft picks in reverse order to the previous year
        standings. In reality, it is a lottery, but the odds follow the same principle.
         """
        # get standings simulated year
        standings = self.db_handler.get_standings_by_simulation_id_and_year(self.simulation_id, self.year)
        # generate draft order reverse to standings
        standings.sort(key=lambda x: x.position, reverse=True)

        # instantiate draft picks
        draft_picks = []

        # 60 picks, 2x standings
        for pick_number, standing in enumerate(standings + standings):
            draft_pick = DraftPickDb(team=standing.team,
                                 pick_number=pick_number + 1,
                                 team_id=standing.team.id,
                                 year=self.year+1,
                                 simulation_id=self.simulation_id)
            draft_picks.append(draft_pick)

        # db writer writes
        self.db_handler.write_entities(draft_picks)
