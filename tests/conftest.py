"""
    Dummy conftest.py for nba_franchise_manager.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest

from GameSimulator import GameSimulator
from db.DBHandler import DBHandler

@pytest.fixture()
def mock_simulation_id():
    return 'abc'

@pytest.fixture()
def game_simulator(mock_simulation_id):
    db_handler = DBHandler()
    gs = GameSimulator(db_handler, mock_simulation_id)
    return gs
