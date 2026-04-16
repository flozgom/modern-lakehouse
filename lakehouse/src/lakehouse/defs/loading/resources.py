from contextlib import contextmanager

import duckdb
from dagster import ConfigurableResource


class DuckLakeResource(ConfigurableResource):
    """DuckDB connection pre-configured with DuckLake catalog and S3 secrets."""

    minio_user: str
    minio_password: str
    minio_bucket: str
    minio_endpoint: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int = 5432

    @property
    def _postgres_conn_string(self) -> str:
        return (
            f"dbname={self.postgres_db} "
            f"user={self.postgres_user} "
            f"password={self.postgres_password} "
            f"host={self.postgres_host} "
            f"port={self.postgres_port}"
        )

    def _init_connection(self, conn: duckdb.DuckDBPyConnection) -> None:
        """Install extensions, create S3 secret, and attach DuckLake catalog."""
        conn.execute("INSTALL ducklake; INSTALL postgres; INSTALL httpfs;")
        conn.execute("LOAD ducklake; LOAD postgres; LOAD httpfs;")
        conn.execute(f"""
            CREATE SECRET minio_secret (
                TYPE s3, KEY_ID '{self.minio_user}', SECRET '{self.minio_password}',
                ENDPOINT '{self.minio_endpoint}', URL_STYLE 'path', USE_SSL false
            )
        """)
        conn.execute(f"""
            ATTACH 'ducklake:postgres:{self._postgres_conn_string}'
            AS ducklake (DATA_PATH 's3://{self.minio_bucket}/ducklake')
        """)
        conn.execute("USE ducklake")

    @contextmanager
    def get_connection(self):
        """Context manager that yields an initialized DuckLake connection."""
        conn = duckdb.connect(":memory:")
        try:
            self._init_connection(conn)
            yield conn
        finally:
            conn.close()
