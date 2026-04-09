FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends gettext-base \
    && rm -rf /var/lib/apt/lists/*

COPY --from=duckdb/duckdb:1.3.1 /duckdb /usr/local/bin/duckdb

COPY init-ducklake.sql /opt/duckdb/init-ducklake.sql
COPY entrypoint.sh /opt/duckdb/entrypoint.sh
RUN chmod +x /opt/duckdb/entrypoint.sh

ENTRYPOINT ["/opt/duckdb/entrypoint.sh"]
