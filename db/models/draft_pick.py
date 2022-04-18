from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from db.models.team import TeamDb


@dataclass
class DraftPickDb:
    __tablename__ = "draft_picks"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    simulation_id: str = field(metadata={"sa": Column(String(250))})
    pick_number: int = field(metadata={"sa": Column("pick_number", Integer, nullable=False)})
    team_id: int = field(metadata={"sa": Column("team_id", Integer, ForeignKey('teams.id'))})
    team: TeamDb = field(metadata={"sa": relationship("Team", lazy='joined')})
    year: int = field(metadata={"sa": Column("year", Integer, nullable=False)})
