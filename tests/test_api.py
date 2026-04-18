import requests
import os
import time

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.json()}")
    assert response.status_code == 200

def test_retrieval_flow():
    # This test assumes there's at least one image in data/images
    # and the crawler has processed it.
    print("Testing retrieval flow...")
    
    # 1. Check if any images are indexed
    # (We might need an internal endpoint for this or just check DB)
    
    # 2. Upload a selfie (using one of the images from data/images as a test)
    # For now, this is a placeholder until we have real images.
    pass

if __name__ == "__main__":
    # Wait for API to be ready
    print("Waiting for API to start...")
    for _ in range(30):
        try:
            test_health()
            print("API is ready!")
            break
        except:
            time.sleep(2)
    else:
        print("API failed to start in time.")
