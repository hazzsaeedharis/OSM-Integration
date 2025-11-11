# FastAPI Backend - Berlin Business Finder

REST API backend for the mobile app.

## Quick Start

### Install Dependencies

```bash
py -m pip install -r requirements-api.txt
```

### Run API Server

```bash
# From project root
cd backend/api
py main.py

# Or with uvicorn directly
py -m uvicorn main:app --reload --port 8000
```

API will be available at: **http://localhost:8000**

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### GET /api/v1/businesses
Get filtered list of businesses

**Query Parameters:**
- `search` - Search term for business name
- `category` - Filter by category
- `city` - Filter by city
- `limit` - Max results (1-500, default: 100)
- `offset` - Pagination offset (default: 0)

**Example:**
```
GET /api/v1/businesses?search=Friseur&limit=50
```

### GET /api/v1/businesses/{id}
Get single business by ID

**Example:**
```
GET /api/v1/businesses/1092037312
```

### GET /api/v1/categories
Get all unique categories

**Example:**
```
GET /api/v1/categories
```

### GET /api/v1/cities
Get all unique cities/districts

**Example:**
```
GET /api/v1/cities
```

### GET /api/v1/statistics
Get database statistics

**Example:**
```
GET /api/v1/statistics
```

### GET /health
Health check endpoint

## Database

Uses existing SQLite database at:
```
backend/data/berlin_businesses.db
```

No additional setup required - the API reuses the existing database!

## CORS

CORS is enabled for all origins during development. For production, update `allow_origins` in `main.py`.

## Port

API runs on port **8000** (Streamlit uses 8501, no conflicts!)

