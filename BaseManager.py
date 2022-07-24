from dataclasses import dataclass
from typing import List

from Logger import Logger
from db.DBHandler import DBHandler
from db.models.player import PlayerDb


@dataclass
class BaseManager:
    db_handler: DBHandler
    simulation_id: str
    logger = Logger()

    def __post_init__(self):
        self.teams_by_team_id = self.db_handler.get_teams_by_team_id()

    @staticmethod
    def clone_model(model):
        """Clone an arbitrary sqlalchemy model object without its primary key values. From
        https://gist.github.com/polozhevets/1c0c97e7c531aeadd077d47bda7ac6cf """
        # Ensure the model’s data is loaded before copying.
        model.id

        table = model.__table__
        non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
        data = {c: getattr(model, c) for c in non_pk_columns}
        data.pop('id', None)  # avoid throwing error if id does not exist
        return data

    def create_new_model(self, entity):
        raise NotImplementedError

    def retrieve_existing_entities(self):
        raise NotImplementedError

    def duplicate_entities_without_sim_id(self):
        """
        Players without simulation_id (written during initial_data) are retrieved, are appended with the
        current simulation_id and finally stored as new objects.
        :return:
        """
        # retrieve players without simulation_id
        new_entities = []
        existing_entities = self.retrieve_existing_entities()
        self.logger.logger.debug(f"Retrieved {len(existing_entities)} entities without simulation_id")
        for old_entity in existing_entities:
            cloned_old_entity = self.clone_model(old_entity)
            new_entity = self.create_new_model(cloned_old_entity)
            new_entity.simulation_id = self.simulation_id
            new_entities.append(new_entity)
        # commit
        self.db_handler.write_entities(new_entities)
