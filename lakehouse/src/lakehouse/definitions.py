from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (one level above lakehouse/)
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

from dagster import Definitions, EnvVar, definitions, load_from_defs_folder
from dagster_dbt import DbtCliResource
from dagster_dlt import DagsterDltResource

from lakehouse.defs.loading.resources import DuckLakeResource
from lakehouse.defs.transform.dbt_assets import dbt_project


@definitions
def defs():
    loaded = load_from_defs_folder(path_within_project=Path(__file__).parent)
    return Definitions(
        assets=loaded.assets,
        resources={
            **(loaded.resources or {}),
            "dlt": DagsterDltResource(),
            "dbt": DbtCliResource(project_dir=dbt_project),
            "ducklake": DuckLakeResource(
                minio_user=EnvVar("MINIO_ROOT_USER"),
                minio_password=EnvVar("MINIO_ROOT_PASSWORD"),
                minio_bucket=EnvVar("MINIO_BUCKET"),
                minio_endpoint=EnvVar("MINIO_ENDPOINT"),
                postgres_user=EnvVar("POSTGRES_USER"),
                postgres_password=EnvVar("POSTGRES_PASSWORD"),
                postgres_db=EnvVar("POSTGRES_DB"),
                postgres_host=EnvVar("POSTGRES_HOST"),
                postgres_port=EnvVar.int("POSTGRES_PORT"),
            ),
        },
    )
