# Task 2: Database Schema & Vector Store

## Objective
Design and implement a relational schema that maps images to multiple unique identities using high-dimensional vectors.

## Schema Design
- **`images` Table**:
  - `id`: UUID (Primary Key)
  - `storage_path`: String (Path to raw image)
  - `processed_at`: Timestamp
- **`faces` Table**:
  - `id`: UUID (Primary Key)
  - `image_id`: UUID (Foreign Key)
  - `grab_id`: UUID (Unique ID for a specific person)
  - `embedding`: `VECTOR(128)` or `VECTOR(512)` (Depending on the model)
  - `bounding_box`: JSONB (x, y, w, h)

## Implementation Details
- SQLAlchemy models for `Image` and `Face`.
- Migrations setup (Alembic or direct scripts).
- HNSW index creation on the `embedding` column for fast similarity search.

## Testing
- [ ] Run migration and verify tables exist.
- [ ] Insert a dummy 128-dim vector and retrieve it using `<->` (L2 distance) or `<=>` (Cosine distance).
