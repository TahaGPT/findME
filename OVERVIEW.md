# Vyro-Backend: Grabpic (Intelligent Identity & Retrieval Engine)

## 1. The Problem: The Marathon Photo Paradox
In large-scale events like marathons with 50,000+ photos and 500+ participants, manual tagging is a logistical nightmare. Photographers capture thousands of moments, but delivering the right photos to the right participant is slow, error-prone, and often results in lost memories.

## 2. The Solution: "Selfie-as-a-Key"
Grabpic transforms photo retrieval into a seamless, automated experience. Instead of searching through galleries, a user simply uploads a selfie. The system uses high-performance facial recognition to "unlock" all photos they appear in.

### Technical Approach:
- **Scalable Ingestion**: A crawler that monitors storage (S3/Local) and feeds images into a processing pipeline.
- **Neural Face Indexing**: Using **RetinaFace** for detection and **FaceNet/ArcFace** embeddings to represent unique identities.
- **Vector-Native Storage**: Leveraging **PostgreSQL with pgvector** to perform high-dimensional similarity searches at sub-second speeds.
- **Identity Synthesis**: Automatically assigning a unique `grab_id` to every unique face discovered, even in complex group shots.

## 3. The "Wow" Factor
- **Sub-Second Retrieval**: Using **HNSW (Hierarchical Navigable Small World)** indexing to ensure that even with 50,000+ photos, a user's collection is found instantly.
- **Zero-Registration Identity**: The system doesn't need a database of "known" users. It discovers and clusters identities on the fly as it processes images.
- **Crowd-Proof Accuracy**: Optimized detection backend capable of finding faces in motion, from side profiles, and within dense crowds.

## 4. Efficiency Strategy
- **Asynchronous Processing**: Decoupling image ingestion from the API response to handle bursts of data.
- **Batch Embedding**: Processing multiple faces within a single image in a vectorized manner to maximize GPU/CPU utilization.
- **Surgical Search**: Using Cosine Similarity thresholds to eliminate false positives while ensuring high recall.

---
*Created for Vyrothon 2026*
