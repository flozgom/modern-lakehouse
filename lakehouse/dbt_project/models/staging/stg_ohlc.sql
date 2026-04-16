select
    pair,
    time_stamp,
    open,
    high,
    low,
    close,
    vwap,
    volume,
    count
from {{ source('ducklake', 'ohlc') }}
