"""
FastAPI Backend for Berlin Business Finder
Provides REST API endpoints for mobile app
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import sqlite3
import json
from pathlib import Path
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Berlin Business Finder API",
    description="REST API for Berlin business data with OpenStreetMap integration",
    version="1.0.0"
)

# Configure CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = Path(__file__).parent.parent / 'data' / 'berlin_businesses.db'

# Pydantic models
class Business(BaseModel):
    id: str
    name: str
    postal_code: str
    city: str
    lat: Optional[float]
    lon: Optional[float]
    categories: List[str]
    branch_ids: List[str]

class BusinessResponse(BaseModel):
    businesses: List[Business]
    total: int
    limit: int
    offset: int

class Statistics(BaseModel):
    total_businesses: int
    geocoded_businesses: int
    unique_postal_codes: int
    unique_cities: int

# Database helper
def get_db_connection():
    """Get database connection"""
    if not DB_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Database not found at {DB_PATH}")
    return sqlite3.connect(DB_PATH)

# API Routes

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Berlin Business Finder API",
        "version": "1.0.0",
        "endpoints": {
            "businesses": "/api/v1/businesses",
            "categories": "/api/v1/categories",
            "cities": "/api/v1/cities",
            "statistics": "/api/v1/statistics",
            "docs": "/docs"
        }
    }

@app.get("/api/v1/businesses", response_model=BusinessResponse)
def get_businesses(
    search: Optional[str] = Query(None, description="Search term for business name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    city: Optional[str] = Query(None, description="Filter by city"),
    limit: int = Query(100, ge=1, le=500, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get businesses with optional filters
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    query = '''
        SELECT id, name, postal_code, city, lat, lon, categories, branch_ids
        FROM businesses
        WHERE lat IS NOT NULL
    '''
    params = []
    
    # Add filters
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')
    
    if category:
        query += ' AND categories LIKE ?'
        params.append(f'%{category}%')
    
    if city:
        query += ' AND city = ?'
        params.append(city)
    
    # Get total count
    count_query = query.replace('SELECT id, name, postal_code, city, lat, lon, categories, branch_ids', 'SELECT COUNT(*)')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Add pagination
    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    # Execute query
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Parse results
    businesses = []
    for row in rows:
        businesses.append(Business(
            id=row[0],
            name=row[1],
            postal_code=row[2],
            city=row[3],
            lat=row[4],
            lon=row[5],
            categories=json.loads(row[6]) if row[6] else [],
            branch_ids=json.loads(row[7]) if row[7] else []
        ))
    
    conn.close()
    
    return BusinessResponse(
        businesses=businesses,
        total=total,
        limit=limit,
        offset=offset
    )

@app.get("/api/v1/businesses/{business_id}", response_model=Business)
def get_business(business_id: str):
    """
    Get single business by ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, postal_code, city, lat, lon, categories, branch_ids
        FROM businesses
        WHERE id = ?
    ''', (business_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return Business(
        id=row[0],
        name=row[1],
        postal_code=row[2],
        city=row[3],
        lat=row[4],
        lon=row[5],
        categories=json.loads(row[6]) if row[6] else [],
        branch_ids=json.loads(row[7]) if row[7] else []
    )

@app.get("/api/v1/categories", response_model=List[str])
def get_categories():
    """
    Get all unique categories
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT categories FROM businesses WHERE categories IS NOT NULL')
    
    categories_set = set()
    for row in cursor.fetchall():
        try:
            cats = json.loads(row[0])
            categories_set.update(cats)
        except:
            pass
    
    conn.close()
    
    return sorted(list(categories_set))

@app.get("/api/v1/cities", response_model=List[str])
def get_cities():
    """
    Get all unique cities
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT city FROM businesses WHERE city IS NOT NULL ORDER BY city')
    cities = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return cities

@app.get("/api/v1/statistics", response_model=Statistics)
def get_statistics():
    """
    Get database statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all stats
    cursor.execute('SELECT key, value FROM statistics')
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    
    return Statistics(
        total_businesses=int(stats.get('total_businesses', 0)),
        geocoded_businesses=int(stats.get('geocoded_businesses', 0)),
        unique_postal_codes=int(stats.get('unique_postal_codes', 0)),
        unique_cities=int(stats.get('unique_cities', 0))
    )

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected" if DB_PATH.exists() else "not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

