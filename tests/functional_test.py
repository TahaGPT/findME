import requests
import time
import os
import sys

BASE_URL = "http://localhost:8000"
DATA_DIR = "./data/images"

def run_test():
    print("--- Vyro-Backend Functional Test ---")
    
    # 1. Health check
    try:
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            print("[PASS] API is healthy.")
        else:
            print(f"[FAIL] API health check returned {r.status_code}")
            return
    except Exception as e:
        print(f"[ERROR] Could not connect to API: {e}")
        print("Ensure the containers are running with 'docker compose up -d'")
        return

    # 2. Prepare test image
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    test_img_path = os.path.join(DATA_DIR, "test_face.jpg")
    sample_url = "https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img1.jpg"
    
    print(f"Downloading sample face to {test_img_path}...")
    img_data = requests.get(sample_url).content
    with open(test_img_path, "wb") as f:
        f.write(img_data)

    # 3. Wait for Crawler
    print("Waiting 45 seconds for the background crawler to index the image...")
    # The crawler runs every 30s as configured in app/main.py
    time.sleep(45)

    # 4. Authenticate (Selfie-as-a-Key)
    print("Testing Selfie Authentication (POST /api/v1/auth/selfie)...")
    with open(test_img_path, "rb") as f:
        files = {"file": ("selfie.jpg", f, "image/jpeg")}
        r = requests.post(f"{BASE_URL}/api/v1/auth/selfie", files=files)
    
    if r.status_code != 200:
        print(f"[FAIL] Authentication failed: {r.text}")
        return
    
    grab_id = r.json().get("grab_id")
    print(f"[PASS] Identity discovered! grab_id: {grab_id}")

    # 5. Retrieve Images
    print(f"Retrieving images for identity {grab_id}...")
    r = requests.get(f"{BASE_URL}/api/v1/images/{grab_id}")
    
    if r.status_code == 200:
        images = r.json().get("images", [])
        print(f"[PASS] Successfully retrieved {len(images)} images.")
        for img in images:
            print(f" - Found at: {img['path']}")
    else:
        print(f"[FAIL] Could not retrieve images: {r.text}")

if __name__ == "__main__":
    run_test()
