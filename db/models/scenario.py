from dataclasses import dataclass, field

from sqlalchemy import String, Column, Integer


@dataclass
class ScenarioDb:
    __tablename__ = 'scenarios'
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column("id", Integer, primary_key=True)})
    scenario_group_id: str = field(metadata={"sa": Column(String(250), nullable=False)})
    simulation_id: str = field(metadata={"sa": Column(String(250), nullable=False)})
