# Task 3: Facial Recognition Engine

## Objective
The core "brain" of Grabpic. Implement the logic to detect faces, generate embeddings, and assign/match `grab_id`s.

## Logic Flow
1. **Detection**: Use `RetinaFace` or `dlib` to find all faces in an image.
2. **Embedding**: Generate a mathematical fingerprint (vector) for each face.
3. **Clustering/Matching**:
   - For each detected face, search the `faces` table for a match (distance < threshold).
   - If a match exists, assign that `grab_id`.
   - If no match exists, generate a new `grab_id`.

## Implementation Details
- Integration with `face_recognition` library or `DeepFace`.
- Helper class `FaceProcessor` for image transformations.
- Threshold tuning (e.g., 0.6 for dlib, 0.4 for ArcFace).

## Testing
- [ ] Process an image with 1 face and verify 1 `grab_id` is created.
- [ ] Process the same image again and verify NO new `grab_id` is created (re-identification).
- [ ] Process an image with 3 people and verify 3 distinct `grab_id`s are mapped to 1 `image_id`.
