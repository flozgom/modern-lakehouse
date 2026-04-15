-- DELETE FROM ducklake.ohlc;
--
-- INSERT INTO ducklake.ohlc
-- SELECT time_stamp, open, high, low, close, vwap, volume, count, pair
-- FROM (
--     SELECT *, ROW_NUMBER() OVER (
--         PARTITION BY pair, time_stamp ORDER BY _dlt_load_id DESC
--     ) AS rn
--     FROM read_parquet('s3://ducklake/raw/kraken/ohlc/*.parquet')
-- ) WHERE rn = 1;


CREATE OR REPLACE TABLE ducklake.ohlc AS
  SELECT time_stamp, open, high, low, close, vwap, volume, count, pair
  FROM (
      SELECT *, ROW_NUMBER() OVER (
          PARTITION BY pair, time_stamp ORDER BY _dlt_load_id DESC
      ) AS rn
      FROM read_parquet('s3://ducklake/raw/kraken/ohlc/*.parquet')
  ) WHERE rn = 1;