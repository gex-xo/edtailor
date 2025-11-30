from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.term import Term
from app.schemas.term import TermCreate, TermResponse

router = APIRouter(prefix="/terms", tags=["terms"])


@router.get("/", response_model=List[TermResponse])
async def get_terms(language: str = 'en', db: AsyncSession = Depends(get_db)):
    """Get all terms, optionally filtered by language."""
    query = select(Term).where(Term.language == language)
    result = await db.execute(query)
    terms = result.scalars().all()
    return terms


@router.get("/{term_id}", response_model=TermResponse)
async def get_term(term_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific term by ID."""
    result = await db.execute(select(Term).where(Term.id == term_id))
    term = result.scalar_one_or_none()

    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Term with id {term_id} not found",
        )

    return term


@router.post("/", response_model=TermResponse, status_code=status.HTTP_201_CREATED)
async def create_term(term_data: TermCreate, db: AsyncSession = Depends(get_db)):
    """Create a new term."""
    term = Term(**term_data.model_dump())
    db.add(term)
    await db.commit()
    await db.refresh(term)
    return term


@router.put("/{term_id}", response_model=TermResponse)
async def update_term(
    term_id: int, term_data: TermCreate, db: AsyncSession = Depends(get_db)
):
    """Update a term."""
    result = await db.execute(select(Term).where(Term.id == term_id))
    term = result.scalar_one_or_none()

    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Term with id {term_id} not found",
        )

    for field, value in term_data.model_dump().items():
        setattr(term, field, value)

    await db.commit()
    await db.refresh(term)
    return term


@router.delete("/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_term(term_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a term."""
    result = await db.execute(select(Term).where(Term.id == term_id))
    term = result.scalar_one_or_none()

    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Term with id {term_id} not found",
        )

    await db.delete(term)
    await db.commit()
