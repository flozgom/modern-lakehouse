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

## Status

This repository is in early bootstrap phase — no application code, build system, or tests exist yet. The .gitignore is configured for Python.
