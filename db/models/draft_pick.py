from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.team import Team


@dataclass
class DraftPick:
    __tablename__ = "draft_picks"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    pick_number: int = field(metadata={"sa": Column("pick_number", Integer, nullable=False)})
    team_id: int = field(metadata={"sa": Column("team_id", Integer, ForeignKey('teams.id'))})
    team: Team = field(metadata={"sa": relationship("Team", lazy='joined')})
    year: int = field(metadata={"sa": Column("year", Integer, nullable=False)})
