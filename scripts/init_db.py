import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import engine, Base
from app.db.models.image import Image
from app.db.models.face import Face
from sqlalchemy import text

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Creating HNSW index...")
    with engine.connect() as conn:
        # Cosine distance (index)
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_faces_embedding_hnsw ON faces USING hnsw (embedding vector_cosine_ops);"))
        conn.commit()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
