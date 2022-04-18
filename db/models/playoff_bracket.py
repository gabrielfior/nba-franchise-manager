from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from db.models.team import Team


@dataclass
class PlayoffBracket:
    __tablename__ = "playoff_brackets"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    simulation_id: str = field(metadata={"sa": Column(String(250))})
    nodes_sep_comma: str = field(metadata={"sa": Column(String(250), nullable=False)})
