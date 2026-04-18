# Vyro-Backend: Grabpic (Intelligent Identity & Retrieval Engine)

Vyro-Backend is a high-performance image processing engine designed for large-scale events like marathons. It automatically indexes faces and allows participants to find their photos using a single selfie.

## Features
- **Zero-Registration Identity**: Automatically discovers and clusters unique identities from raw images.
- **Selfie-as-a-Key**: Secure and instant photo retrieval via facial recognition.
- **High-Performance Vector Search**: Uses PostgreSQL `pgvector` with HNSW indexing for sub-second retrieval.
- **Asynchronous Ingestion**: Background crawler monitors storage and indexes photos in real-time.

## Tech Stack
- **API**: FastAPI (Python)
- **Database**: PostgreSQL + pgvector
- **AI Engine**: DeepFace (RetinaFace + Facenet512)
- **Infrastructure**: Docker & Docker Compose

## Getting Started

### 1. Prerequisites
- Docker and Docker Compose (v2+)

### 2. Run the System
```bash
# Start the database and API
docker compose up -d

# Initialize the database (tables and vector indexes)
docker run --network vyro_default --env-file .env -e DATABASE_URL=postgresql://vyro_user:vyro_password@db/vyro_db -e PYTHONPATH=/app vyro-init
```

### 3. Usage
- **Add Photos**: Drop `.jpg` or `.png` images into the `./data/images` directory. The background crawler will automatically detect and index all faces.
- **Find Your Photos**:
  - Use `POST /api/v1/auth/selfie` with your selfie image to get your unique `grab_id`.
  - Use `GET /api/v1/images/{grab_id}` to retrieve the list of photos you appear in.

## API Documentation
Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure
- `app/api`: API endpoints and routing.
- `app/db`: Database models and session management.
- `app/services`: Core logic (Face processing, Identity matching, Crawler).
- `data/images`: Target directory for photo ingestion.
- `scripts`: Database initialization and maintenance scripts.
# Vyro-Backend
