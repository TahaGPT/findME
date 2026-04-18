# Task 5: Selfie Authentication & Retrieval API

## Objective
Implement the "Selfie-as-a-Key" feature where a user retrieves their identity and photos.

## Endpoints
1. **`POST /auth/selfie`**:
   - Input: Image file (Selfie).
   - Action: Detect face, generate embedding, search DB for closest match.
   - Output: `grab_id` (Authorizer).
2. **`GET /images/{grab_id}`**:
   - Input: `grab_id`.
   - Action: Fetch all `image_id`s associated with this `grab_id`.
   - Output: List of image URLs/Paths.

## Implementation Details
- Similarity search using `ORDER BY embedding <=> :search_vector LIMIT 1`.
- Error handling for "No face detected" or "Identity not found".

## Testing
- [ ] Upload a selfie of a person already in the system and verify it returns their correct `grab_id`.
- [ ] Fetch images for that `grab_id` and verify they contain the person.
- [ ] Test with a "stranger" selfie (no match) and ensure it returns a 404/Unauthorized.
