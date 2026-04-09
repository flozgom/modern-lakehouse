#!/bin/sh
envsubst < /opt/duckdb/init-ducklake.sql > /tmp/init-ducklake.sql
exec duckdb "$@"
