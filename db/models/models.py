from sqlalchemy.orm import registry

from db.models.draft_pick import DraftPickDb
from db.models.game import GameDb
from db.models.game_mapper import GameMapperDb
from db.models.game_stats import GameStatsDb

from db.models.player import PlayerDb
from db.models.playoff_bracket import PlayoffBracketDb
from db.models.standing import StandingDb
from db.models.team import TeamDb

mapper_registry = registry()
mapper_registry.mapped(DraftPickDb)
mapper_registry.mapped(TeamDb)
mapper_registry.mapped(PlayerDb)
mapper_registry.mapped(GameDb)
mapper_registry.mapped(StandingDb)
mapper_registry.mapped(GameMapperDb)
mapper_registry.mapped(PlayoffBracketDb)
mapper_registry.mapped(GameStatsDb)


# ToDo - Add draft positioning table, for first year should be hardcoded
