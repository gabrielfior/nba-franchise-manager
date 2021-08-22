import datetime
from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.models.team import Team


@dataclass
class Standing:
    __tablename__ = 'standings'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    simulation_id: str = field(metadata={"sa": Column(String(250))})
    year: int = field(metadata={"sa": Column(Integer, nullable=False)})
    team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'), nullable=False)})
    team: Team = field(metadata={"sa": relationship("Team", lazy='joined')})
    position: int = field(metadata={"sa": Column(Integer)})
    conference: str = field(metadata={"sa": Column(String, nullable=False)})
    division: str = field(metadata={"sa": Column(String, nullable=False)})
