from typing import Any

import dlt
import requests


KRAKEN_BASE_URL = "https://api.kraken.com"


def normalize_fields(pair: str, raw_rows: list[list[Any]]) -> list[dict[str, Any]]:
    columns = ["time_stamp", "open", "high", "low", "close", "vwap", "volume", "count"]
    records = []
    for row in raw_rows:
        record = dict(zip(columns, row))
        record["pair"] = pair
        record["open"] = float(record["open"])
        record["high"] = float(record["high"])
        record["low"] = float(record["low"])
        record["close"] = float(record["close"])
        record["vwap"] = float(record["vwap"])
        record["volume"] = float(record["volume"])
        records.append(record)
    return records


@dlt.source
def kraken_source(
    ohlc_pairs: list[str] = dlt.config.value,
):
    yield ohlc(ohlc_pairs)


@dlt.resource(
    primary_key=["pair", "time_stamp"],
    write_disposition="merge",
)
def ohlc(pairs: list[str]):
    for pair in pairs:
        response = requests.get(
            f"{KRAKEN_BASE_URL}/0/public/OHLC",
            params={"pair": pair, "interval": 1440},
        )
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            raise ValueError(f"Kraken API error for {pair}: {data['error']}")

        result = data.get("result", {})
        for key, rows in result.items():
            if key == "last":
                continue
            yield from normalize_fields(pair, rows)
