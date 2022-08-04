from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Float


@dataclass
class DraftPickStatsDb:
    __tablename__ = "draft_pick_stats"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    pick_number: int = field(metadata={"sa": Column("pick_number", Integer, nullable=False)})
    year: int = field(metadata={"sa": Column("year", Integer, nullable=False)})
    points_per_game_mean: float = field(metadata={"sa": Column(Float, nullable=False)})
    points_per_game_std: float = field(metadata={"sa": Column(Float, nullable=False)})

    rebounds_per_game_mean: float = field(metadata={"sa": Column(Float, nullable=False)})
    rebounds_per_game_std: float = field(metadata={"sa": Column(Float, nullable=False)})

    assists_per_game_mean: float = field(metadata={"sa": Column(Float, nullable=False)})
    assists_per_game_std: float = field(metadata={"sa": Column(Float, nullable=False)})

