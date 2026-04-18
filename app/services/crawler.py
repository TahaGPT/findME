import os
import hashlib
import time
from sqlalchemy.orm import Session
from .identity_service import IdentityService

class StorageCrawler:
    def __init__(self, storage_path: str, identity_service: IdentityService):
        self.storage_path = storage_path
        self.identity_service = identity_service

    @staticmethod
    def get_checksum(file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def crawl(self):
        """
        Scans the storage directory for new images and processes them.
        """
        print(f"Starting crawl on {self.storage_path}...")
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            print(f"Created storage directory: {self.storage_path}")

        supported_extensions = (".jpg", ".jpeg", ".png")
        
        for root, _, files in os.walk(self.storage_path):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        checksum = self.get_checksum(file_path)
                        print(f"Processing {file}...")
                        self.identity_service.process_image(file_path, checksum)
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")

    def run_forever(self, interval: int = 10):
        while True:
            self.crawl()
            time.sleep(interval)
