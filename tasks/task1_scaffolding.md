# Task 1: Project Scaffolding & Environment Setup

## Objective
Establish a robust, containerized development environment with all necessary dependencies for vector search and image processing.

## Requirements
- **Docker Compose**: Setup for PostgreSQL with the `pgvector` extension.
- **FastAPI Core**: Initial project structure with modular routing.
- **Environment Management**: `.env` configuration for DB credentials, storage paths, and similarity thresholds.

## Implementation Details
- Use `ankane/pgvector` Docker image.
- Setup Python virtual environment with `fastapi`, `uvicorn`, `sqlalchemy`, and `psycopg2-binary`.
- Initial health-check endpoint.

## Testing
- [ ] Verify `pgvector` extension is enabled in Postgres: `CREATE EXTENSION IF NOT EXISTS vector;`
- [ ] Verify FastAPI container connects to Postgres.
- [ ] Verify `.env` variables are correctly loaded.
