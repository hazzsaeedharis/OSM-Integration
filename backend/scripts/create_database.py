"""
Create SQLite database from geocoded Berlin businesses
"""

import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_creation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_database_schema(conn):
    """Create database schema"""
    logger.info("Creating database schema...")
    
    cursor = conn.cursor()
    
    # Create businesses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            postal_code TEXT,
            city TEXT,
            lat REAL,
            lon REAL,
            categories TEXT,
            branch_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_postal_code ON businesses(postal_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_city ON businesses(city)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_lat_lon ON businesses(lat, lon)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON businesses(name)')
    
    # Create full-text search virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS businesses_fts USING fts5(
            id UNINDEXED,
            name,
            categories,
            content=businesses,
            content_rowid=rowid
        )
    ''')
    
    conn.commit()
    logger.info("Database schema created successfully")

def insert_businesses(conn, businesses):
    """Insert businesses into database"""
    logger.info(f"Inserting {len(businesses):,} businesses...")
    
    cursor = conn.cursor()
    inserted_count = 0
    skipped_count = 0
    
    for i, business in enumerate(businesses):
        try:
            # Convert categories list to JSON string
            categories_json = json.dumps(business.get('categories', []))
            branch_ids_json = json.dumps(business.get('branch_ids', []))
            
            cursor.execute('''
                INSERT OR REPLACE INTO businesses 
                (id, name, postal_code, city, lat, lon, categories, branch_ids)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                business.get('id', ''),
                business.get('name', ''),
                business.get('postal_code', ''),
                business.get('city', ''),
                business.get('lat'),
                business.get('lon'),
                categories_json,
                branch_ids_json
            ))
            
            inserted_count += 1
            
            # Progress logging
            if (i + 1) % 10000 == 0:
                logger.info(f"Progress: {i + 1:,}/{len(businesses):,} businesses inserted...")
                conn.commit()  # Commit in batches
        
        except sqlite3.Error as e:
            logger.warning(f"Failed to insert business {business.get('name')}: {e}")
            skipped_count += 1
            continue
    
    # Final commit
    conn.commit()
    
    # Update FTS index
    logger.info("Updating full-text search index...")
    cursor.execute('''
        INSERT INTO businesses_fts(rowid, id, name, categories)
        SELECT rowid, id, name, categories FROM businesses
    ''')
    conn.commit()
    
    logger.info("="*60)
    logger.info(f"Database population complete!")
    logger.info(f"  Inserted: {inserted_count:,}")
    logger.info(f"  Skipped: {skipped_count:,}")
    logger.info("="*60)

def create_statistics_table(conn):
    """Create a statistics table with metadata"""
    logger.info("Creating statistics table...")
    
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM businesses')
    total_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE lat IS NOT NULL')
    geocoded_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT postal_code) FROM businesses')
    unique_postcodes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT city) FROM businesses')
    unique_cities = cursor.fetchone()[0]
    
    # Create stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert statistics
    stats = [
        ('total_businesses', str(total_count)),
        ('geocoded_businesses', str(geocoded_count)),
        ('unique_postal_codes', str(unique_postcodes)),
        ('unique_cities', str(unique_cities)),
        ('database_version', '1.0'),
        ('last_updated', datetime.now().isoformat())
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO statistics (key, value) VALUES (?, ?)', stats)
    conn.commit()
    
    logger.info(f"Statistics:")
    logger.info(f"  Total businesses: {total_count:,}")
    logger.info(f"  Geocoded: {geocoded_count:,}")
    logger.info(f"  Unique postal codes: {unique_postcodes}")
    logger.info(f"  Unique cities: {unique_cities}")

def optimize_database(conn):
    """Optimize database"""
    logger.info("Optimizing database...")
    
    cursor = conn.cursor()
    cursor.execute('VACUUM')
    cursor.execute('ANALYZE')
    
    conn.commit()
    logger.info("Database optimized")

def main():
    """Main database creation process"""
    start_time = datetime.now()
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'backend' / 'data'
    
    input_path = data_dir / 'berlin_businesses_geocoded.json'
    db_path = data_dir / 'berlin_businesses.db'
    
    logger.info("="*60)
    logger.info("Berlin Business Database Creation")
    logger.info("="*60)
    logger.info(f"Input file: {input_path}")
    logger.info(f"Database file: {db_path}")
    
    try:
        # Load geocoded data
        logger.info("Loading geocoded businesses...")
        with open(input_path, 'r', encoding='utf-8') as f:
            businesses = json.load(f)
        logger.info(f"Loaded {len(businesses):,} businesses")
        
        # Remove existing database
        if db_path.exists():
            logger.info("Removing existing database...")
            db_path.unlink()
        
        # Create database
        logger.info("Connecting to database...")
        conn = sqlite3.connect(db_path)
        
        # Create schema
        create_database_schema(conn)
        
        # Insert businesses
        insert_businesses(conn, businesses)
        
        # Create statistics
        create_statistics_table(conn)
        
        # Optimize
        optimize_database(conn)
        
        # Close connection
        conn.close()
        
        # Summary
        elapsed_time = (datetime.now() - start_time).total_seconds()
        db_size = db_path.stat().st_size / (1024 * 1024)
        
        logger.info("\n" + "="*60)
        logger.info("DATABASE CREATION COMPLETE!")
        logger.info("="*60)
        logger.info(f"Database file: {db_path}")
        logger.info(f"Database size: {db_size:.2f} MB")
        logger.info(f"Execution time: {elapsed_time:.2f} seconds")
        
        # Test query
        logger.info("\nTesting database query...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, city, postal_code, lat, lon 
            FROM businesses 
            WHERE lat IS NOT NULL 
            LIMIT 3
        ''')
        
        logger.info("\nSample query results:")
        for row in cursor.fetchall():
            logger.info(f"  {row[0]} - {row[1]} ({row[2]}) - {row[3]:.6f}, {row[4]:.6f}")
        
        conn.close()
        
        logger.info("\nLog file created: database_creation.log")
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return 1
    except Exception as e:
        logger.error(f"FATAL ERROR: Database creation failed - {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

