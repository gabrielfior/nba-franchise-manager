import datetime
from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.models.team import TeamDb


@dataclass
class GameDb:
    __tablename__ = 'games'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    year: int = field(metadata={"sa": Column(Integer, nullable=False)})
    simulation_id: str = field(metadata={"sa": Column(String(250))})
    game_type: str = field(metadata={"sa": Column(String(250), nullable=False)})
    home_team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'), nullable=False)})
    home_team: TeamDb = field(
        metadata={"sa": relationship("Team", foreign_keys=[home_team_id.metadata['sa']], lazy='joined')})

    away_team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'), nullable=False)})
    away_team: TeamDb = field(metadata={"sa": relationship("Team", foreign_keys=[away_team_id.metadata['sa']], lazy='joined')})
    game_date: datetime.date = field(metadata={"sa": Column(Date, nullable=False)})
    home_team_points: int = field(metadata={"sa": Column(Integer)}, default_factory=int)
    away_team_points: int = field(metadata={"sa": Column(Integer)}, default_factory=int)
