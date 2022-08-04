from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from db.models.team import TeamDb


@dataclass
class GameMapperDb:
    __tablename__ = 'game_mapper'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    home_team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'))})
    away_team_id: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.id'))})
