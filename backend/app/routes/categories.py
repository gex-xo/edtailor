from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.category import Category
from app.models.topic import Topic
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.topic import TopicResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(language: str = 'en', db: AsyncSession = Depends(get_db)):
    """Get all categories, optionally filtered by language."""
    query = select(Category).where(Category.language == language)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific category by ID."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )

    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new category."""
    category = Category(**category_data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, category_data: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    """Update a category."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )

    for field, value in category_data.model_dump().items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a category."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )

    await db.delete(category)
    await db.commit()


@router.get("/{category_id}/topics", response_model=List[TopicResponse])
async def get_category_topics(
    category_id: int, language: str = 'en', db: AsyncSession = Depends(get_db)
):
    """Get all topics for a specific category."""
    # First check if category exists
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )

    # Get topics for this category filtered by language
    query = select(Topic).where(
        (Topic.category_id == category_id) & (Topic.language == language)
    )
    result = await db.execute(query)
    topics = result.scalars().all()
    return topics
