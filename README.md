# Notes App Backend API

A secure multi-user Notes Management Backend built using **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.  
This project provides REST APIs for user authentication, note management, note sharing, and note searching.

---

# Live Deployment

## Base URL
https://notes-app-0952.onrender.com

## Swagger API Docs
https://notes-app-0952.onrender.com/docs

## OpenAPI JSON
https://notes-app-0952.onrender.com/openapi.json

---

# Features

## User Authentication
- User Registration
- Secure Login using JWT Authentication
- Password Hashing using bcrypt

## Notes Management
- Create Notes
- Read Notes
- Update Notes
- Delete Notes

## Note Sharing
- Share notes securely with another registered user
- Shared users can access notes via note ID

## Custom Feature
### Search Notes
Implemented keyword-based note searching for improved usability and faster note retrieval.

---

# Tech Stack

| Technology | Usage |
|---|---|
| FastAPI | Backend Framework |
| SQLAlchemy | ORM |
| SQLite | Database |
| JWT | Authentication |
| bcrypt | Password Hashing |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |
| Render | Deployment |

---

# Project Structure

```bash
notes-app/
│
├── main.py
├── models.py
├── schemas.py
├── auth.py
├── database.py
├── requirements.txt
├── README.md
└── notes.db
```

---

# API Endpoints

## Authentication

### Register User
```http
POST /register
```

Request Body:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

### Login User
```http
POST /login
```

Request Body:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "jwt_token"
}
```

---

# Notes APIs

### Create Note
```http
POST /notes
```

### Get All Notes
```http
GET /notes
```

### Get Note by ID
```http
GET /notes/{id}
```

### Update Note
```http
PUT /notes/{id}
```

### Delete Note
```http
DELETE /notes/{id}
```

---

# Share Notes

### Share a Note
```http
POST /notes/{id}/share
```

Request Body:

```json
{
  "share_with_email": "friend@example.com"
}
```

---

# Search Notes Feature

### Search Notes by Keyword
```http
GET /search?q=keyword
```

Example:

```text
/search?q=python
```

---

# About Endpoint

### About API
```http
GET /about
```

Response:

```json
{
  "name": "Sourav Subham",
  "email": "redsouravsubham@gmail.com",
  "my_features": {
    "Search Notes": "Added keyword-based note searching functionality for better usability."
  }
}
```

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/Sourav93-subh/notes-app.git
```

```bash
cd notes-app
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Server

```bash
uvicorn main:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

---

# Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Protected routes using Bearer Token
- Ownership validation for notes
- Shared note access control

---

# Deployment

The application is deployed on Render.

## Deployment URL
https://notes-app-0952.onrender.com

---

# Author

## Sourav Subham

- Email: redsouravsubham@gmail.com
- GitHub: https://github.com/Sourav93-subh

---

# Future Improvements

- Pagination for notes
- Full-text search
- Docker support
- Frontend integration
- PostgreSQL migration
- Role-based permissions

---

# License

This project is built for educational and assessment purposes.