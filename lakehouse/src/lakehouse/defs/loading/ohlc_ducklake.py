from pathlib import Path

from dagster import AssetKey, asset
from lakehouse.defs.loading.resources import DuckLakeResource

LOAD_SQL = (Path(__file__).parent / "load_ohlc.sql").read_text()


@asset(
    deps=[AssetKey(["kraken", "ohlc"])],
    group_name="loading",
)
def ohlc_ducklake(context, ducklake: DuckLakeResource):
    """Load deduplicated OHLC data from raw parquet files into DuckLake."""
    with ducklake.get_connection() as conn:
        conn.execute(LOAD_SQL)
        count = conn.execute("SELECT count(*) FROM ducklake.ohlc").fetchone()[0]
        context.log.info(f"Loaded {count} rows into ducklake.ohlc")
