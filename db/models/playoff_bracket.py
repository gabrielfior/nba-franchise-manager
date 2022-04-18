from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, String


@dataclass
class PlayoffBracketDb:
    __tablename__ = "playoff_brackets"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    simulation_id: str = field(metadata={"sa": Column(String(250))})
    year: int = field(metadata={"sa": Column("year", Integer, nullable=False)})
    nodes_sep_comma: str = field(metadata={"sa": Column(String(250), nullable=False)})
