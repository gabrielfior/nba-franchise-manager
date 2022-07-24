import datetime
from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.models.team import TeamDb


@dataclass
class VegasOddsDb:
    __tablename__ = 'vegas_odds'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    year: int = field(metadata={"sa": Column(Integer, nullable=False)})
    team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'), nullable=False)})
    team: TeamDb = field(metadata={"sa": relationship("TeamDb", lazy='joined')})
    odd_rank:int = field(metadata={"sa": Column(Integer, nullable=False)})
