# EdTailor - Fashion Education Platform

EdTailor is a comprehensive web application for learning about fashion, tailoring, fabrics, styling, and garment construction.

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose

## Project Structure

```
edtailor/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration & database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── static/         # Static files & images
│   │   └── main.py         # FastAPI application
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile
│   └── .env               # Environment variables
└── docker-compose.yml      # Docker orchestration
```

## Database Schema

- **Categories**: Top-level content organization
- **Topics**: Subjects within categories
- **Lessons**: Educational content
- **Fabrics**: Fabric reference library
- **Garments**: Clothing encyclopedia
- **Terms**: Fashion terminology glossary
- **Tags**: Cross-referencing system

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git (optional)

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd edtailor
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Running Migrations

Migrations run automatically when starting the container. To run manually:

```bash
docker-compose exec backend alembic upgrade head
```

### Creating a New Migration

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## API Endpoints

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}` - Get specific category
- `POST /api/categories/` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Lessons
- `GET /api/lessons/` - List all lessons
- `GET /api/lessons/{id}` - Get specific lesson
- `POST /api/lessons/` - Create lesson
- `PUT /api/lessons/{id}` - Update lesson
- `DELETE /api/lessons/{id}` - Delete lesson

### Fabrics
- `GET /api/fabrics/` - List all fabrics
- `GET /api/fabrics/{id}` - Get specific fabric
- `POST /api/fabrics/` - Create fabric
- `PUT /api/fabrics/{id}` - Update fabric
- `DELETE /api/fabrics/{id}` - Delete fabric

## Development

### Stopping the Application

```bash
docker-compose down
```

### Viewing Logs

```bash
docker-compose logs -f backend
```

### Accessing the Database

```bash
docker-compose exec db psql -U edtailor -d edtailor_db
```

## Adding Content

Content can be added through:
1. API endpoints (using the /docs interface)
2. Python scripts
3. Database seed files
4. Direct database access

## Future Features

- Additional entity routes (Garments, Terms, Tags)
- Search functionality
- Frontend interface
- Image upload support
- Content filtering and pagination

## License

Private educational project
