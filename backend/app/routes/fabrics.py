from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.fabric import Fabric
from app.schemas.fabric import FabricCreate, FabricResponse

router = APIRouter(prefix="/fabrics", tags=["fabrics"])


@router.get("/", response_model=List[FabricResponse])
async def get_fabrics(language: str = 'en', db: AsyncSession = Depends(get_db)):
    """Get all fabrics, optionally filtered by language."""
    query = select(Fabric).where(Fabric.language == language)
    result = await db.execute(query)
    fabrics = result.scalars().all()
    return fabrics


@router.get("/{fabric_id}", response_model=FabricResponse)
async def get_fabric(fabric_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific fabric by ID."""
    result = await db.execute(select(Fabric).where(Fabric.id == fabric_id))
    fabric = result.scalar_one_or_none()

    if not fabric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fabric with id {fabric_id} not found",
        )

    return fabric


@router.post("/", response_model=FabricResponse, status_code=status.HTTP_201_CREATED)
async def create_fabric(fabric_data: FabricCreate, db: AsyncSession = Depends(get_db)):
    """Create a new fabric."""
    fabric = Fabric(**fabric_data.model_dump())
    db.add(fabric)
    await db.commit()
    await db.refresh(fabric)
    return fabric


@router.put("/{fabric_id}", response_model=FabricResponse)
async def update_fabric(
    fabric_id: int, fabric_data: FabricCreate, db: AsyncSession = Depends(get_db)
):
    """Update a fabric."""
    result = await db.execute(select(Fabric).where(Fabric.id == fabric_id))
    fabric = result.scalar_one_or_none()

    if not fabric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fabric with id {fabric_id} not found",
        )

    for field, value in fabric_data.model_dump().items():
        setattr(fabric, field, value)

    await db.commit()
    await db.refresh(fabric)
    return fabric


@router.delete("/{fabric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fabric(fabric_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a fabric."""
    result = await db.execute(select(Fabric).where(Fabric.id == fabric_id))
    fabric = result.scalar_one_or_none()

    if not fabric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fabric with id {fabric_id} not found",
        )

    await db.delete(fabric)
    await db.commit()
