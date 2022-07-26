from dataclasses import dataclass

from BaseManager import BaseManager
from Logger import Logger
from db.DBHandler import DBHandler
from db.models.player import PlayerDb


@dataclass
class PlayerExpander:
    db_handler: DBHandler
    simulation_id: str
    year: int
    n_years: int
    logger = Logger()

    def __post_init__(self):
        self.teams_by_team_id = self.db_handler.get_teams_by_team_id()

    def retrieve_existing_entities(self):
        # should be executed after PlayerManager has been run
        return self.db_handler.get_all(PlayerDb, [('simulation_id', self.simulation_id),
                                                  ('year_drafted', self.year)])

    def create_new_model(self, entity: dict, year: int):
        team = self.teams_by_team_id[entity['team_id']]
        entity['team'] = team
        p = PlayerDb(**entity)
        p.year_drafted = year
        return p

    def expand_entities(self):
        """
        We copy a player's stats from self.year to years [self.year+1, self.year+n_years]
        """
        # retrieve players without simulation_id
        new_entities = []
        existing_entities = self.retrieve_existing_entities()
        self.logger.logger.debug(f"Retrieved {len(existing_entities)} entities without simulation_id")
        years_to_expand_into = list(range(self.year+1, self.year + self.n_years))
        for year_to_store, entities_curr_year in zip(years_to_expand_into, [existing_entities]*len(years_to_expand_into)):
            for old_entity in entities_curr_year:
                cloned_old_entity = BaseManager.clone_model(old_entity)
                new_entity = self.create_new_model(cloned_old_entity, year_to_store)
                new_entity.simulation_id = self.simulation_id
                new_entities.append(new_entity)
        # commit
        self.db_handler.write_entities(new_entities)
