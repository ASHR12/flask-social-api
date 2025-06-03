# Social Media REST API Documentation

Base URL:
```
http://127.0.0.1:5000/
```

---

## Authentication

### Register a New User
- **Endpoint:** `POST /api/auth/register`
- **Request Body:**
  ```json
  {
    "username": "yourname",
    "email": "your@email.com",
    "password": "yourpassword",
    "bio": "optional bio",
    "avatar_url": "optional avatar url"
  }
  ```
- **Response:**
  - `201 Created` on success
  - `409 Conflict` if username/email exists
  - `400 Bad Request` with validation errors

**Example (curl):**
```sh
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@email.com","password":"password123"}'
```

---

### Login
- **Endpoint:** `POST /api/auth/login`
- **Request Body:**
  ```json
  {
    "username": "yourname",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "JWT_TOKEN",
    "user": {
      "id": 1,
      "username": "alice",
      "email": "alice@email.com",
      "bio": "",
      "avatar_url": ""
    }
  }
  ```
  - `401 Unauthorized` if credentials are invalid

**Example (curl):**
```sh
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

---

## User Profile

### Get User Profile
- **Endpoint:** `GET /api/users/<user_id>`
- **Response:**
  ```json
  {
    "id": 1,
    "username": "alice",
    "email": "alice@email.com",
    "bio": "",
    "avatar_url": "",
    "followers": 2,
    "following": 3,
    "posts": 5
  }
  ```

**Example (curl):**
```sh
curl http://127.0.0.1:5000/api/users/1
```

---

### Update Your Profile
- **Endpoint:** `PUT /api/users/<user_id>`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "bio": "New bio",
    "avatar_url": "https://example.com/avatar.png"
  }
  ```
- **Response:**
  ```json
  { "message": "Profile updated." }
  ```

**Example (curl):**
```sh
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"bio":"New bio"}'
```

---

## Posts

### Create a Post
- **Endpoint:** `POST /api/posts`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "title": "My Post",
    "content": "This is the content."
  }
  ```
- **Response:**
  ```json
  { "message": "Post created.", "post_id": 10 }
  ```

**Example (curl):**
```sh
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"This is the content."}'
```

---

### Get a Post
- **Endpoint:** `GET /api/posts/<post_id>`
- **Response:**
  ```json
  {
    "id": 10,
    "author": "alice",
    "title": "My Post",
    "content": "This is the content.",
    "timestamp": "2024-06-01T12:00:00",
    "likes": 2,
    "comments": 3
  }
  ```

**Example (curl):**
```sh
curl http://127.0.0.1:5000/api/posts/10
```

---

### Update a Post
- **Endpoint:** `PUT /api/posts/<post_id>`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:** (any fields to update)
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content."
  }
  ```
- **Response:**
  ```json
  { "message": "Post updated." }
  ```

---

### Delete a Post
- **Endpoint:** `DELETE /api/posts/<post_id>`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  { "message": "Post deleted." }
  ```

---

## Likes

### Like a Post
- **Endpoint:** `POST /api/posts/<post_id>/like`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  { "message": "Post liked." }
  ```

---

### Unlike a Post
- **Endpoint:** `POST /api/posts/<post_id>/unlike`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  { "message": "Post unliked." }
  ```

---

## Comments

### Add a Comment
- **Endpoint:** `POST /api/posts/<post_id>/comments`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  { "content": "Nice post!" }
  ```
- **Response:**
  ```json
  { "message": "Comment added.", "comment_id": 5 }
  ```

---

### Get Comments for a Post
- **Endpoint:** `GET /api/posts/<post_id>/comments`
- **Response:**
  ```json
  [
    {
      "id": 5,
      "author": "bob",
      "content": "Nice post!",
      "timestamp": "2024-06-01T12:05:00"
    }
  ]
  ```

---

## Follow/Unfollow

### Follow a User
- **Endpoint:** `POST /api/users/<user_id>/follow`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  { "message": "Now following user." }
  ```

---

### Unfollow a User
- **Endpoint:** `POST /api/users/<user_id>/unfollow`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  { "message": "Unfollowed user." }
  ```

---

## Feed

### Get Your Feed
- **Endpoint:** `GET /api/feed`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  [
    {
      "id": 10,
      "author": "bob",
      "title": "Bob's Post",
      "content": "Hello world!",
      "timestamp": "2024-06-01T12:00:00",
      "likes": 2,
      "comments": 1
    }
  ]
  ```

---

## Root

- **Endpoint:** `GET /`
- **Response:**
  ```json
  {
    "message": "Welcome to the Social Media REST API.",
    "docs": "See /api or /api/auth for available endpoints."
  }
  ```

---

## Notes
- All endpoints that modify or access user-specific data require the `Authorization: Bearer <JWT_TOKEN>` header.
- Use the JWT token received from the login endpoint for all protected routes.
- All request and response bodies are in JSON format.
- User IDs and post IDs are integers, as returned by the API.
