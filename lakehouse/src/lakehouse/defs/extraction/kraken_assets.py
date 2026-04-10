import dlt
from dagster_dlt import DagsterDltResource, dlt_assets

from lakehouse.sources.kraken import kraken_source


@dlt_assets(
    dlt_source=kraken_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="kraken_ohlc",
        dataset_name="kraken",
        destination=dlt.destinations.filesystem(
            bucket_url="s3://ducklake/raw",
            layout="{table_name}/{load_id}.{file_id}.{ext}",
        ),
    ),
    name="kraken",
    group_name="extraction",
)
def kraken_assets(context, dlt: DagsterDltResource):
    yield from dlt.run(context=context, loader_file_format="parquet")
