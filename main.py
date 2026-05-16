from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime

import models
import schemas

from database import SessionLocal, engine
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# JWT Security
security = HTTPBearer()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get Current Logged-in User
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        user = db.query(models.User).filter(
            models.User.id == user_id
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ----------------------------------------
# Register User
# ----------------------------------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# ----------------------------------------
# Login User
# ----------------------------------------
@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": token
    }


# ----------------------------------------
# Create Note
# ----------------------------------------
@app.post("/notes")
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    new_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# ----------------------------------------
# Get All Notes
# ----------------------------------------
@app.get("/notes")
def get_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    notes = db.query(models.Note).filter(
        models.Note.owner_id == current_user.id
    ).all()

    return notes


# ----------------------------------------
# Get Note By ID
# ----------------------------------------
@app.get("/notes/{id}")
def get_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    note = db.query(models.Note).filter(
        models.Note.id == id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    # Check ownership
    if note.owner_id != current_user.id:

        # Check shared access
        shared_note = db.query(models.SharedNote).filter(
            models.SharedNote.note_id == id,
            models.SharedNote.user_id == current_user.id
        ).first()

        if not shared_note:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return note


# ----------------------------------------
# Update Note
# ----------------------------------------
@app.put("/notes/{id}")
def update_note(
    id: int,
    updated_note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    note = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content
    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note


# ----------------------------------------
# Delete Note
# ----------------------------------------
@app.delete("/notes/{id}")
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    note = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }


# ----------------------------------------
# Share Note
# ----------------------------------------
@app.post("/notes/{id}/share")
def share_note(
    id: int,
    share: schemas.ShareNote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    note = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    user_to_share = db.query(models.User).filter(
        models.User.email == share.share_with_email
    ).first()

    if not user_to_share:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    already_shared = db.query(models.SharedNote).filter(
        models.SharedNote.note_id == id,
        models.SharedNote.user_id == user_to_share.id
    ).first()

    if already_shared:
        raise HTTPException(
            status_code=400,
            detail="Note already shared with this user"
        )

    shared_note = models.SharedNote(
        note_id=id,
        user_id=user_to_share.id
    )

    db.add(shared_note)
    db.commit()

    return {
        "message": "Note shared successfully"
    }


# ----------------------------------------
# Search Notes (Custom Feature)
# ----------------------------------------
@app.get("/search")
def search_notes(
    q: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    notes = db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        models.Note.title.contains(q)
    ).all()

    return notes


# ----------------------------------------
# About Endpoint
# ----------------------------------------
@app.get("/about")
def about():

    return {
        "name": "Sourav Subham",
        "email": "redsouravsubham@gmail.com",
        "my_features": {
            "Search Notes":
            "Added keyword-based note searching functionality for better usability."
        }
    }