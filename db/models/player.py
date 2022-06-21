from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from db.models.team import TeamDb


@dataclass
class PlayerDb:
    __tablename__ = 'players'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column("id", Integer, primary_key=True)}
    )
    name: str = field(metadata={"sa": Column(String, nullable=False)})
    team_id: int = field(metadata={"sa": Column("team_id", Integer, ForeignKey('teams.id'))})
    team: TeamDb = field(metadata={"sa": relationship("TeamDb")})

    year_drafted: int = field(metadata={"sa": Column(Integer, nullable=False)})
    age: int = field(metadata={"sa": Column(Integer, nullable=False)})
    points_per_game: float = field(metadata={"sa": Column(Float, nullable=False)})
    rebounds_per_game: float = field(metadata={"sa": Column(Float, nullable=False)})
    assists_per_game: float = field(metadata={"sa": Column(Float, nullable=False)})
    simulation_id: str = field(metadata={"sa": Column(String(250), nullable=True)})
