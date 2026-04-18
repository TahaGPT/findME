from fastapi import FastAPI, BackgroundTasks
from .api.endpoints import retrieval
from .services.crawler import StorageCrawler
from .services.identity_service import IdentityService
from .services.face_processor import FaceProcessor
from .db.session import SessionLocal
import os
import threading

app = FastAPI(title="Vyro-Backend: Grabpic")

# Include routers
app.include_router(retrieval.router, prefix="/api/v1", tags=["retrieval"])

def start_crawler():
    db = SessionLocal()
    face_processor = FaceProcessor()
    identity_service = IdentityService(db, face_processor)
    storage_path = os.getenv("STORAGE_PATH", "./data/images")
    crawler = StorageCrawler(storage_path, identity_service)
    crawler.run_forever(interval=30)

@app.on_event("startup")
async def startup_event():
    # Run crawler in a separate thread to not block the API
    thread = threading.Thread(target=start_crawler, daemon=True)
    thread.start()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "vyro-api"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Vyro-Backend: Grabpic"}
