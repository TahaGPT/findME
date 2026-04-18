from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import uuid
from ..db.models.image import Image
from ..db.models.face import Face
from .face_processor import FaceProcessor
import os

MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", 0.45))

class IdentityService:
    def __init__(self, db: Session, face_processor: FaceProcessor):
        self.db = db
        self.face_processor = face_processor

    def find_matching_grab_id(self, embedding: list) -> Optional[uuid.UUID]:
        """
        Uses pgvector similarity search to find the closest face.
        Returns grab_id if distance is within threshold.
        """
        # Cosine distance operator <=> returns 1 - cosine_similarity
        query = text("""
            SELECT grab_id, embedding <=> :emb as distance
            FROM faces
            ORDER BY distance ASC
            LIMIT 1
        """)
        
        result = self.db.execute(query, {"emb": str(embedding)}).fetchone()
        
        if result and result.distance < MATCH_THRESHOLD:
            return result.grab_id
        return None

    def process_image(self, image_path: str, checksum: str):
        """
        Full pipeline for a single image.
        """
        # Check if image already processed
        existing_image = self.db.query(Image).filter(Image.checksum == checksum).first()
        if existing_image:
            return existing_image

        # 1. Extract faces
        faces_data = self.face_processor.extract_faces(image_path)
        
        # 2. Create Image record
        new_image = Image(storage_path=image_path, checksum=checksum)
        self.db.add(new_image)
        self.db.flush() # Get ID

        # 3. Process each face
        for face_info in faces_data:
            embedding = face_info["embedding"]
            box = face_info["box"]
            
            grab_id = self.find_matching_grab_id(embedding)
            
            if not grab_id:
                grab_id = self.face_processor.generate_grab_id()
                print(f"Created new identity: {grab_id}")
            else:
                print(f"Matched existing identity: {grab_id}")

            face_record = Face(
                image_id=new_image.id,
                grab_id=grab_id,
                embedding=embedding,
                bounding_box=box
            )
            self.db.add(face_record)

        self.db.commit()
        return new_image
