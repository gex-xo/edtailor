from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import categories, lessons, fabrics, garments, terms

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="EdTailor - Fashion Education Platform API",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(categories.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(fabrics.router, prefix="/api")
app.include_router(garments.router, prefix="/api")
app.include_router(terms.router, prefix="/api")

# Mount frontend
app.mount("/js", StaticFiles(directory="/frontend/js"), name="js")


@app.get("/")
async def root():
    """Serve the frontend application."""
    return FileResponse("/frontend/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
