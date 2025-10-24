from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.diary import Post
from app.models.user import User

router = APIRouter(prefix="/diary", tags=["diary"])


@router.post("/", response_model=dict)
async def create_diary(title: str, content: str, user: User = Depends(get_current_user)):
    post = Post(title=title, content=content, date=date.today(), author=user)
    await post.save()
    user.number_of_posts += 1
    await user.save()
    return {"id": post.id, "title": post.title, "content": post.content}


@router.get("/", response_model=List[dict])
async def get_diaries():
    posts = await Post.all().prefetch_related("author")
    return [{"id": p.id, "title": p.title, "author": p.author.username} for p in posts]


@router.get("/{diary_id}", response_model=dict)
async def get_diary(diary_id: int):
    post = await Post.filter(id=diary_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Diary not found")
    return {"id": post.id, "title": post.title, "content": post.content}


@router.put("/{diary_id}")
async def update_diary(diary_id: int, title: str, content: str, user: User = Depends(get_current_user)):
    post = await Post.filter(id=diary_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Diary not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post.title = title
    post.content = content
    await post.save()
    return {"message": "updated"}


@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, user: User = Depends(get_current_user)):
    post = await Post.filter(id=diary_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Diary not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await post.delete()
    user.number_of_posts = max(0, user.number_of_posts - 1)
    await user.save()
    return {"message": "deleted"}
