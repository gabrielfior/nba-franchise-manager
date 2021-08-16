from sqlalchemy.orm import registry

from db.models.draft_pick import DraftPick
from db.models.game import Game
from db.models.game_mapper import GameMapper

from db.models.player import Player
from db.models.standing import Standing
from db.models.team import Team

mapper_registry = registry()
mapper_registry.mapped(DraftPick)
mapper_registry.mapped(Team)
mapper_registry.mapped(Player)
mapper_registry.mapped(Game)

mapper_registry.mapped(Standing)
mapper_registry.mapped(GameMapper)


# ToDo - Add draft positioning table, for first year should be hardcoded
