from dataclasses import dataclass, field
from typing import List

from sqlalchemy import String, Column, Integer


@dataclass
class Team:
    __tablename__ = 'teams'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String, nullable=False, unique=True)})
    short_name: str = field(metadata={"sa": Column(String, nullable=False)})
    conference: str = field(metadata={"sa": Column(String, nullable=False)})
    division: str = field(metadata={"sa": Column(String, nullable=False)})
