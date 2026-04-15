import subprocess
from pathlib import Path

from dagster import AssetKey, asset

COMPOSE_FILE = str(Path(__file__).resolve().parents[5] / "docker-compose.yml")
LOAD_SQL = (Path(__file__).parent / "load_ohlc.sql").read_text()


@asset(
    deps=[AssetKey(["kraken", "ohlc"])],
    group_name="loading",
)
def ohlc_ducklake(context):
    """Load deduplicated OHLC data from raw parquet files into DuckLake."""
    result = subprocess.run(
        [
            "docker", "compose", "-f", COMPOSE_FILE,
            "run", "--rm", "--no-TTY", "duckdb",
            "-c", ".read /tmp/init-ducklake.sql",
            "-c", LOAD_SQL,
        ],
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"DuckDB load failed:\n{result.stderr}")
