ATTACH 'dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} host=postgres port=5432' AS pg (TYPE POSTGRES);

CALL postgres_execute('pg', 'CREATE SCHEMA IF NOT EXISTS silver');

CALL postgres_execute('pg', '
    CREATE TABLE IF NOT EXISTS silver.ohlc (
        pair VARCHAR,
        time_stamp BIGINT,
        open DOUBLE PRECISION,
        high DOUBLE PRECISION,
        low DOUBLE PRECISION,
        close DOUBLE PRECISION,
        vwap DOUBLE PRECISION,
        volume DOUBLE PRECISION,
        count BIGINT,
        PRIMARY KEY (pair, time_stamp)
    )
');

CALL postgres_execute('pg', 'TRUNCATE silver.ohlc');

INSERT INTO pg.silver.ohlc (pair, time_stamp, open, high, low, close, vwap, volume, count)
SELECT pair, time_stamp, open, high, low, close, vwap, volume, count
FROM ducklake.ohlc;
