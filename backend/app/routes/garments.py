from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.garment import Garment
from app.schemas.garment import GarmentCreate, GarmentResponse

router = APIRouter(prefix="/garments", tags=["garments"])


@router.get("/", response_model=List[GarmentResponse])
async def get_garments(language: str = 'en', db: AsyncSession = Depends(get_db)):
    """Get all garments, optionally filtered by language."""
    query = select(Garment).where(Garment.language == language)
    result = await db.execute(query)
    garments = result.scalars().all()
    return garments


@router.get("/{garment_id}", response_model=GarmentResponse)
async def get_garment(garment_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific garment by ID."""
    result = await db.execute(select(Garment).where(Garment.id == garment_id))
    garment = result.scalar_one_or_none()

    if not garment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Garment with id {garment_id} not found",
        )

    return garment


@router.post("/", response_model=GarmentResponse, status_code=status.HTTP_201_CREATED)
async def create_garment(garment_data: GarmentCreate, db: AsyncSession = Depends(get_db)):
    """Create a new garment."""
    garment = Garment(**garment_data.model_dump())
    db.add(garment)
    await db.commit()
    await db.refresh(garment)
    return garment


@router.put("/{garment_id}", response_model=GarmentResponse)
async def update_garment(
    garment_id: int, garment_data: GarmentCreate, db: AsyncSession = Depends(get_db)
):
    """Update a garment."""
    result = await db.execute(select(Garment).where(Garment.id == garment_id))
    garment = result.scalar_one_or_none()

    if not garment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Garment with id {garment_id} not found",
        )

    for field, value in garment_data.model_dump().items():
        setattr(garment, field, value)

    await db.commit()
    await db.refresh(garment)
    return garment


@router.delete("/{garment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_garment(garment_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a garment."""
    result = await db.execute(select(Garment).where(Garment.id == garment_id))
    garment = result.scalar_one_or_none()

    if not garment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Garment with id {garment_id} not found",
        )

    await db.delete(garment)
    await db.commit()
