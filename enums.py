from enum import Enum


class GameTypes(Enum):
    REGULAR_SEASON = 'REGULAR_SEASON'
    CONF_QUARTER_FINALS = 'CONF_QUARTER_FINALS'
    CONF_SEMIS = 'CONF_SEMIS'
    CONF_FINALS = 'CONF_FINALS'
    FINALS = 'FINALS'


class Conferences(Enum):
    EAST = 'EAST'
    WEST = 'WEST'


class PlayerStatus(Enum):
    TRADED = 'traded'
    EXISTING = 'existing'
    DRAFTED = 'drafted'
