from datetime import timedelta

import pandas as pd
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float64, Int64

player = Entity(
    name="player",
    join_keys=["player_id"],
)

source = FileSource(
    name="player_deposits_source",
    path="data/player_deposits.parquet",
    timestamp_field="event_timestamp",
)

player_features = FeatureView(
    name="player_features",
    entities=[player],
    ttl=timedelta(days=365),
    schema=[
        Field(name="avg_deposit", dtype=Float64),
    ],
    source=source,
)
