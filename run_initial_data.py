from db.DBHandler import DBHandler
from db.initial_migration.initial_data_filler import InitialDataFiller

if __name__ == "__main__":
    delete_initial_data = False
    create_initial_data = True

    db_handler = DBHandler(echo=True)
    draft_year = 2021

    # add initial data
    idf = InitialDataFiller(draft_year, db_handler)
    if delete_initial_data:
        idf.delete_initial_data()
    if create_initial_data:
        idf.insert_initial_data()
