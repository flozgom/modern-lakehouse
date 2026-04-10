# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Modern data lakehouse built on DuckLake. The target architecture is:

- **Kafka** topic as the ingestion entry point
- **Kafka Connect** with an S3-compatible sink writing to **MinIO**
- **DuckLake** as the lakehouse layer on top of MinIO storage
- **PostgreSQL** as the DuckLake catalog

## Development

```bash
# Copy env template and adjust if needed
cp .env.example .env

# Start infrastructure (MinIO + PostgreSQL)
docker compose up -d

# Open interactive DuckDB shell connected to the lakehouse
docker compose run --rm duckdb

# Inside DuckDB, run the init script to set up extensions and attach catalog
# .read /tmp/init-ducklake.sql

# Tear down
docker compose down
# Tear down and delete volumes
docker compose down -v
```

## Dagster (Data Orchestration)

The `lakehouse/` directory contains a Dagster project scaffolded with `dg`. It uses `dlt` to extract data and write Parquet files to MinIO.

```bash
cd lakehouse

# Install dependencies (uses uv)
uv sync --group dev

# Copy dlt secrets and adjust if needed
cp .dlt/secrets.toml.example .dlt/secrets.toml

# Ensure infrastructure is running
docker compose -f ../docker-compose.yml up -d

# Launch Dagster dev UI
uv run dagster dev

# Materialize assets from CLI
uv run dagster asset materialize --select kraken/ohlc
```

### dlt Configuration

- `.dlt/config.toml` — destination config (filesystem/MinIO, parquet format)
- `.dlt/secrets.toml` — credentials and source config (not committed)
- `.dlt/secrets.toml.example` — template for secrets

## Status

Bootstrap phase with Dagster + dlt extraction pipeline targeting MinIO.
