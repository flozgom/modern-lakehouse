import subprocess
from pathlib import Path

from dagster import AssetKey, asset

COMPOSE_FILE = str(Path(__file__).resolve().parents[5] / "docker-compose.yml")


@asset(
    deps=[AssetKey("ohlc_ducklake")],
    group_name="loading",
)
def ohlc_silver(context):
    """Upsert OHLC from DuckLake into PostgreSQL silver layer."""
    result = subprocess.run(
        [
            "docker", "compose", "-f", COMPOSE_FILE,
            "run", "--rm", "--no-TTY", "duckdb",
            "-c", ".read /tmp/init-ducklake.sql",
            "-c", ".read /tmp/upsert_ohlc_silver.sql",
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"Silver upsert failed:\n{result.stderr}")
