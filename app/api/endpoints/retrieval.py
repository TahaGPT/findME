from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from typing import List
from ...db.session import get_db
from ...services.identity_service import IdentityService
from ...services.face_processor import FaceProcessor
from ...db.models.face import Face
from ...db.models.image import Image

router = APIRouter()
face_processor = FaceProcessor()

@router.post("/auth/selfie")
async def authenticate_selfie(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save temporary file
    temp_path = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        identity_service = IdentityService(db, face_processor)
        faces = face_processor.extract_faces(temp_path)
        
        if not faces:
            raise HTTPException(status_code=400, detail="No face detected in selfie")
        
        # Take the largest face if multiple detected
        main_face = max(faces, key=lambda f: f["box"]["w"] * f["box"]["h"])
        grab_id = identity_service.find_matching_grab_id(main_face["embedding"])
        
        if not grab_id:
            raise HTTPException(status_code=404, detail="Identity not found. Are you in the marathon photos?")
        
        return {"grab_id": grab_id, "status": "authorized"}
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/images/{grab_id}")
async def get_user_images(grab_id: uuid.UUID, db: Session = Depends(get_db)):
    faces = db.query(Face).filter(Face.grab_id == grab_id).all()
    if not faces:
        raise HTTPException(status_code=404, detail="No images found for this identity")
    
    results = []
    for face in faces:
        results.append({
            "image_id": face.image_id,
            "path": face.image.storage_path,
            "bounding_box": face.bounding_box
        })
    
    return {"grab_id": grab_id, "images": results}
