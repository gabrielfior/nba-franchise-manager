from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.models.game import GameDb


@dataclass
class GameStatsDb:
    __tablename__ = 'game_stats'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})

    game_id: int = field(metadata={"sa": Column("game_id", Integer, ForeignKey('games.id'))})
    # add lazy='subquery' if game object needs to be retrieved
    game: GameDb = field(metadata={"sa": relationship("GameDb")})
    points_scored: float = field(metadata={"sa": Column(Integer, nullable=False)})

    player_id: int = field(metadata={"sa": Column("player_id", Integer, ForeignKey('players.id'))})


