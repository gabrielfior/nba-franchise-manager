from sqlalchemy.orm import registry

from db.models.draft_pick import DraftPickDb
from db.models.game import GameDb
from db.models.game_mapper import GameMapperDb
from db.models.game_stats import GameStatsDb

from db.models.player import PlayerDb
from db.models.playoff_bracket import PlayoffBracketDb
from db.models.scenario import ScenarioDb
from db.models.standing import StandingDb
from db.models.team import TeamDb
from db.models.draft_pick_stats import DraftPickStatsDb

mapper_registry = registry()
mapper_registry.mapped(DraftPickDb)
mapper_registry.mapped(TeamDb)
mapper_registry.mapped(PlayerDb)
mapper_registry.mapped(GameDb)
mapper_registry.mapped(StandingDb)
mapper_registry.mapped(GameMapperDb)
mapper_registry.mapped(PlayoffBracketDb)
mapper_registry.mapped(GameStatsDb)
mapper_registry.mapped(ScenarioDb)
mapper_registry.mapped(DraftPickStatsDb)


# ToDo - Add draft positioning table, for first year should be hardcoded
