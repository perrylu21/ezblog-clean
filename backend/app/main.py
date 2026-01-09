import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from .database import Base, engine, get_db
from .models import BlogPost


app = FastAPI(title="ezblog API", version="0.1.0")

# Configure CORS origins from environment variable or use defaults
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    # Split comma-separated origins from environment variable
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]
else:
    # Default origins for local development
    cors_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostCreate(BaseModel):
    title: str
    content: str


class PostRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.post(
    "/posts",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    tags=["posts"],
)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    post = BlogPost(title=payload.title, content=payload.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts", response_model=List[PostRead], tags=["posts"])
def list_posts(db: Session = Depends(get_db)):
    stmt = select(BlogPost).order_by(BlogPost.id.desc())
    posts = db.execute(stmt).scalars().all()
    return posts


@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["posts"],
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(BlogPost, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    db.delete(post)
    db.commit()
    # 204 No Content: return an empty body
    return None

