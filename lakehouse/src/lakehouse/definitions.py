from pathlib import Path

from dagster import Definitions, definitions, load_from_defs_folder
from dagster_dlt import DagsterDltResource


@definitions
def defs():
    loaded = load_from_defs_folder(path_within_project=Path(__file__).parent)
    return Definitions(
        assets=loaded.assets,
        resources={**(loaded.resources or {}), "dlt": DagsterDltResource()},
    )
