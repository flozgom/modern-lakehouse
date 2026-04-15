#!/bin/sh
for f in /opt/duckdb/*.sql; do
    envsubst < "$f" > "/tmp/$(basename "$f")"
done
exec duckdb "$@"
