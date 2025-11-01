from datetime import datetime
from typing import List, Optional

from pytz import timezone

from app.models.diary import Post
from app.models.question import Question
from app.models.questions import Questions
from app.models.user import User


# 일기 생성
async def create_diary(
    user: User, title: str, content: str, question_id: int, question_answer: str
) -> Post:
    pool_q = await Questions.get(id=question_id)

    # 질문 생성
    question = await Question.create(content=pool_q.content, answer=question_answer)

    # Post 생성 시 question을 연결
    post = await Post.create(
        title=title,
        content=content,
        date=datetime.now(),
        author=user,
        question=question,
    )

    # 사용자 게시글 수 업데이트
    user.number_of_posts += 1
    await user.save()
    return post


# 특정 일기 조회
async def get_diary(post_id: int, user: User) -> Optional[Post]:
    post = await Post.filter(id=post_id, author=user).select_related("question").first()
    return post


# 일기 목록 조회 (월별/연도별)
async def get_diaries(
    user: User,
    month: Optional[int] = None,
    year: Optional[int] = None,
) -> List[Post]:

    now = datetime.now(timezone("Asia/Seoul"))
    target_year = year or now.year
    target_month = month

    query = Post.filter(author=user, created_at__year=target_year)

    if target_month:
        query = query.filter(created_at__month=target_month)

    return await query.order_by("-created_at").prefetch_related("question").all()


# 일기 수정
async def update_diary(
    post: Post,
    title: Optional[str] = None,
    content: Optional[str] = None,
    question_answer: Optional[str] = None,
) -> Post:
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
