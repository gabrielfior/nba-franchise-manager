from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Enum, String

allowed_descriptions = ['IN_CONFERENCE_OUTSIDE_DIVISION',
                        'IN_CONFERECE_INSIDE_DIVISION',
                        'OUT_OF_CONFERENCE']


class GameDescription(Enum):
    IN_CONFERENCE_IN_DIVISION = 'IN_CONFERENCE_IN_DIVISION'
    IN_CONFERENCE_OUT_OF_DIVISION = 'IN_CONFERENCE_OUT_OF_DIVISION'
    OUT_OF_CONFERENCE = 'OUT_OF_CONFERENCE'


@dataclass
class GameType:
    __tablename__ = 'game_types'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    description: str = field(metadata={"sa": Column(String, nullable=False)})
