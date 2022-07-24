from dataclasses import dataclass

from BaseManager import BaseManager
from db.models.draft_pick import DraftPickDb


@dataclass
class DraftPickManager(BaseManager):
    def create_new_model(self, entity: dict):
        team = self.teams_by_team_id[entity['team_id']]
        entity['team'] = team
        p = DraftPickDb(**entity)
        return p

    def retrieve_existing_entities(self):
        return self.db_handler.get_all(DraftPickDb, [('simulation_id', None)])
