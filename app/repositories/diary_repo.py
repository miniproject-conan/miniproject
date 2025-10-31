from datetime import datetime, date, timedelta
from typing import List, Optional

from app.models.diary import Post
from app.models.user import User
from app.models.question import Question
from app.models.questions import Questions

# 일기 생성
async def create_diary(user: User, title: str, content: str, question_id: int, question_answer: str) -> Post:
    pool_q = await Questions.get(id=question_id)
    post = await Post.create(
        title=title,
        content=content,
        date=datetime.now(),
        author=user
    )
    await Question.create(
        content=pool_q.content,
        answer=question_answer,
        post=post
    )
    user.number_of_posts += 1
    await user.save()
    return post

# 특정 일기 조회
async def get_diary(post_id: int, user: User) -> Optional[Post]:
    return await Post.filter(id=post_id, author=user).prefetch_related('question').first()

# 일기 목록 조회 (월별/주별)
async def get_diaries(user: User, month: Optional[int] = None, year: Optional[int] = None, week: Optional[int] = None) -> List[Post]:
    query = Post.filter(author=user)

    if year and month:
        query = query.filter(date__year=year, date__month=month)
    elif year and week:
        first_day = date.fromisocalendar(year, week, 1)
        last_day = first_day + timedelta(days=6)
        query = query.filter(date__gte=first_day, date__lte=last_day)

    return await query.order_by("-date").prefetch_related("question").all()

# 일기 수정
async def update_diary(post: Post, title: Optional[str] = None, content: Optional[str] = None, question_answer: Optional[str] = None) -> Post:
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    post.date = datetime.now()
    await post.save()

    if question_answer is not None:
        question = await post.question
        if question:
            question.answer = question_answer
            await question.save()

    return post

# 일기 삭제
async def delete_diary(post: Post, user: User):
    await post.delete()
    user.number_of_posts = max(0, user.number_of_posts - 1)
    await user.save()
