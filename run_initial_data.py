import uuid

from DraftSimulator import DraftSimulator
from GameSimulator import GameSimulator
from ScenarioSimulator import ScenarioSimulator
from ScheduleSimulator import ScheduleSimulator

from db.DBHandler import DBHandler
from db.initial_migration.initial_data_filler import InitialDataFiller

if __name__ == "__main__":
    create_initial_data = True
    delete_initial_data = False

    db_handler = DBHandler()
    draft_year = 2021

    # add initial data
    idf = InitialDataFiller(draft_year, db_handler)
    if create_initial_data:
        idf.insert_initial_data()
    if delete_initial_data:
        idf.delete_initial_data()