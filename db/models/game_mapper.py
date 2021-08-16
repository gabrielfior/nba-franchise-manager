import datetime
from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.models.team import Team


@dataclass
class GameMapper:
    __tablename__ = 'game_mapper'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    home_team_short_name: int = field(metadata={"sa": Column(String, ForeignKey('teams.short_name'), nullable=False)})
    away_team_short_name: int = field(metadata={"sa": Column(Integer, ForeignKey('teams.short_name'), nullable=False)})

