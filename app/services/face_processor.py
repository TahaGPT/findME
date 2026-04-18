import uuid
import numpy as np
from deepface import DeepFace
from typing import List, Dict, Any
import os

class FaceProcessor:
    def __init__(self, model_name: str = "Facenet512", detector_backend: str = "retinaface"):
        self.model_name = model_name
        self.detector_backend = detector_backend

    def extract_faces(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Detects faces and generates embeddings for each.
        Returns a list of dicts with 'embedding' and 'box'.
        """
        try:
            results = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            
            extracted = []
            for res in results:
                extracted.append({
                    "embedding": res["embedding"],
                    "box": res["facial_area"]  # {'x': 10, 'y': 20, 'w': 30, 'h': 40}
                })
            return extracted
        except Exception as e:
            print(f"Error extracting faces from {image_path}: {e}")
            return []

    @staticmethod
    def generate_grab_id() -> uuid.UUID:
        return uuid.uuid4()
