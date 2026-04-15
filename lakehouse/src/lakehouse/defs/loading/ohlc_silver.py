from dagster import AssetKey, asset
from lakehouse.defs.loading.resources import DuckLakeResource


@asset(
    deps=[AssetKey("ohlc_ducklake")],
    group_name="loading",
)
def ohlc_silver(context, ducklake: DuckLakeResource):
    """Upsert OHLC from DuckLake into PostgreSQL silver layer."""
    with ducklake.get_connection() as conn:
        conn.execute(f"""
            ATTACH 'postgres:{ducklake._postgres_conn_string}'
            AS pg (TYPE POSTGRES)
        """)
        conn.execute("CALL postgres_execute('pg', 'CREATE SCHEMA IF NOT EXISTS silver')")
        conn.execute("""CALL postgres_execute('pg', '
            CREATE TABLE IF NOT EXISTS silver.ohlc (
                pair VARCHAR, time_stamp BIGINT,
                open DOUBLE PRECISION, high DOUBLE PRECISION,
                low DOUBLE PRECISION, close DOUBLE PRECISION,
                vwap DOUBLE PRECISION, volume DOUBLE PRECISION,
                count BIGINT, PRIMARY KEY (pair, time_stamp)
            )')""")
        conn.execute("CALL postgres_execute('pg', 'TRUNCATE silver.ohlc')")
        conn.execute("""
            INSERT INTO pg.silver.ohlc
            SELECT pair, time_stamp, open, high, low, close, vwap, volume, count
            FROM ducklake.ohlc
        """)
        count = conn.execute("SELECT count(*) FROM pg.silver.ohlc").fetchone()[0]
        context.log.info(f"Upserted {count} rows into silver.ohlc")
