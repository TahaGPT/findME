# Task 4: Ingestion & Discovery Pipeline

## Objective
Automate the process of crawling storage and indexing new images.

## Requirements
- **Storage Crawler**: A service that scans a target directory or S3 bucket for new `.jpg`, `.png` files.
- **Indexing Service**: Logic to prevent duplicate processing of the same file.
- **Batch Processing**: Ability to process images in chunks to manage memory.

## Implementation Details
- File system observer (e.g., `watchdog`) or simple polling.
- Checksum (MD5/SHA) of images to avoid re-processing if moved.
- Background worker (Task queue like Celery or simple `BackgroundTasks` in FastAPI).

## Testing
- [ ] Drop 10 images into the folder and verify the API starts processing them.
- [ ] Verify `images` table is populated with correct storage paths.
