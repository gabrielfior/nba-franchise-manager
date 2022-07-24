from dataclasses import dataclass

from BaseManager import BaseManager
from db.models.player import PlayerDb
from enums import PlayerStatus


@dataclass
class PlayerManager(BaseManager):

    def create_new_model(self, entity: dict):
        team = self.teams_by_team_id[entity['team_id']]
        entity['team'] = team
        p = PlayerDb(**entity)
        return p

    def retrieve_existing_entities(self):
        return self.db_handler.get_all(PlayerDb, [('simulation_id', None)])
