{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key=['pair', 'trade_date']
    )
}}

select
    pair,
    cast(to_timestamp(time_stamp) as date) as trade_date,
    arg_min(open, time_stamp) as open,
    max(high) as high,
    min(low) as low,
    arg_max(close, time_stamp) as close,
    sum(volume) as volume,
    sum(count) as trade_count
from {{ ref('stg_ohlc') }}
{% if is_incremental() %}
where time_stamp > (select max(time_stamp) from {{ this }})
{% endif %}
group by pair, trade_date
