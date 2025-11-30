from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.lesson import Lesson
from app.models.topic import Topic
from app.schemas.lesson import LessonCreate, LessonResponse

router = APIRouter(tags=["lessons"])


@router.get("/lessons", response_model=List[LessonResponse])
async def get_lessons(db: AsyncSession = Depends(get_db)):
    """Get all lessons."""
    result = await db.execute(select(Lesson))
    lessons = result.scalars().all()
    return lessons


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific lesson by ID."""
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with id {lesson_id} not found",
        )

    return lesson


@router.post("/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson_data: LessonCreate, db: AsyncSession = Depends(get_db)):
    """Create a new lesson."""
    lesson = Lesson(**lesson_data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int, lesson_data: LessonCreate, db: AsyncSession = Depends(get_db)
):
    """Update a lesson."""
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with id {lesson_id} not found",
        )

    for field, value in lesson_data.model_dump().items():
        setattr(lesson, field, value)

    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a lesson."""
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with id {lesson_id} not found",
        )

    await db.delete(lesson)
    await db.commit()


@router.get("/topics/{topic_id}/lessons", response_model=List[LessonResponse])
async def get_topic_lessons(
    topic_id: int, language: str = 'en', db: AsyncSession = Depends(get_db)
):
    """Get all lessons for a specific topic."""
    # First check if topic exists
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found",
        )

    # Get lessons for this topic filtered by language
    query = select(Lesson).where(
        (Lesson.topic_id == topic_id) & (Lesson.language == language)
    )
    result = await db.execute(query)
    lessons = result.scalars().all()
    return lessons
