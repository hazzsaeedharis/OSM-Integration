"""
Update Berlin businesses with precise coordinates and additional data
from berlin_business_data.jsonl
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
        logging.FileHandler('data_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_precise_data(jsonl_path):
    """Load data from berlin_business_data.jsonl"""
    logger.info(f"Loading precise data from {jsonl_path}...")
    
    data_map = {}
    total_count = 0
    with_coords = 0
    with_street = 0
    with_phone = 0
    with_email = 0
    with_website = 0
    
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total_count += 1
                
                if total_count % 10000 == 0:
                    logger.info(f"Processed {total_count:,} records...")
                
                try:
                    record = json.loads(line.strip())
                    teilnehmer = record.get('antwort', {}).get('daten', {}).get('teilnehmer', {})
                    
                    if not teilnehmer:
                        continue
                    
                    business_id = teilnehmer.get('id', '')
                    if not business_id:
                        continue
                    
                    # Extract address data
                    adresse = teilnehmer.get('adresse', {})
                    kontakt = teilnehmer.get('kontakt', {})
                    
                    # Get coordinates
                    geodaten = adresse.get('geodaten', {})
                    koordinaten = geodaten.get('koordinaten', [])
                    
                    lat, lon = None, None
                    for coord in koordinaten:
                        if coord.get('format') == 'WGS84':
                            lon = float(coord.get('x', 0))
                            lat = float(coord.get('y', 0))
                            with_coords += 1
                            break
                    
                    # Get street address
                    street = adresse.get('anzeige_strasse', adresse.get('strasse', ''))
                    hausnr = adresse.get('hausnr', '')
                    full_address = f"{street} {hausnr}".strip() if street else None
                    if full_address:
                        with_street += 1
                    
                    # Get district
                    district = adresse.get('stadtteil', '')
                    
                    # Get phone
                    telefon_list = kontakt.get('telefon', [])
                    phone = None
                    if telefon_list:
                        phone = telefon_list[0].get('rufnummer', '')
                        if phone:
                            with_phone += 1
                    
                    # Get email
                    email_list = kontakt.get('email', [])
                    email = None
                    if email_list:
                        email = email_list[0].get('email', '')
                        if email:
                            with_email += 1
                    
                    # Get website
                    www_list = kontakt.get('www', [])
                    website = None
                    if www_list:
                        website = www_list[0].get('url', '')
                        if website:
                            with_website += 1
                    
                    # Store data
                    data_map[business_id] = {
                        'lat': lat,
                        'lon': lon,
                        'street_address': full_address,
                        'district': district,
                        'phone': phone,
                        'email': email,
                        'website': website
                    }
                    
                except json.JSONDecodeError as e:
                    logger.debug(f"Line {line_num}: JSON decode error")
                    continue
                except Exception as e:
                    logger.debug(f"Line {line_num}: Error - {e}")
                    continue
        
        logger.info("="*60)
        logger.info(f"Data loading complete!")
        logger.info(f"Total records processed: {total_count:,}")
        logger.info(f"Businesses with data: {len(data_map):,}")
        logger.info(f"  With coordinates: {with_coords:,}")
        logger.info(f"  With street address: {with_street:,}")
        logger.info(f"  With phone: {with_phone:,}")
        logger.info(f"  With email: {with_email:,}")
        logger.info(f"  With website: {with_website:,}")
        logger.info("="*60)
        
        return data_map
    
    except FileNotFoundError:
        logger.error(f"File not found: {jsonl_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}", exc_info=True)
        raise

def update_database(db_path, data_map):
    """Update database with precise data"""
    logger.info(f"Updating database at {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add new columns if they don't exist
    logger.info("Adding new columns to database...")
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN street_address TEXT')
    except sqlite3.OperationalError:
        logger.info("street_address column already exists")
    
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN district TEXT')
    except sqlite3.OperationalError:
        logger.info("district column already exists")
    
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN phone TEXT')
    except sqlite3.OperationalError:
        logger.info("phone column already exists")
    
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN email TEXT')
    except sqlite3.OperationalError:
        logger.info("email column already exists")
    
    try:
        cursor.execute('ALTER TABLE businesses ADD COLUMN website TEXT')
    except sqlite3.OperationalError:
        logger.info("website column already exists")
    
    conn.commit()
    
    # Update businesses
    logger.info("Updating business records...")
    updated_count = 0
    coords_updated = 0
    
    cursor.execute('SELECT id FROM businesses')
    all_ids = [row[0] for row in cursor.fetchall()]
    
    for i, business_id in enumerate(all_ids):
        if (i + 1) % 10000 == 0:
            logger.info(f"Progress: {i + 1:,}/{len(all_ids):,} businesses...")
            conn.commit()
        
        if business_id in data_map:
            data = data_map[business_id]
            
            # Update with new data (only if we have it)
            updates = []
            params = []
            
            if data['lat'] and data['lon']:
                updates.append('lat = ?')
                updates.append('lon = ?')
                params.extend([data['lat'], data['lon']])
                coords_updated += 1
            
            if data['street_address']:
                updates.append('street_address = ?')
                params.append(data['street_address'])
            
            if data['district']:
                updates.append('district = ?')
                params.append(data['district'])
            
            if data['phone']:
                updates.append('phone = ?')
                params.append(data['phone'])
            
            if data['email']:
                updates.append('email = ?')
                params.append(data['email'])
            
            if data['website']:
                updates.append('website = ?')
                params.append(data['website'])
            
            if updates:
                params.append(business_id)
                query = f"UPDATE businesses SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                updated_count += 1
    
    conn.commit()
    
    logger.info("="*60)
    logger.info(f"Database update complete!")
    logger.info(f"  Total businesses updated: {updated_count:,}")
    logger.info(f"  Coordinates updated: {coords_updated:,}")
    logger.info("="*60)
    
    # Update statistics
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE street_address IS NOT NULL')
    with_street = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE phone IS NOT NULL')
    with_phone = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE lat IS NOT NULL')
    with_coords_total = cursor.fetchone()[0]
    
    logger.info("Final Statistics:")
    logger.info(f"  Businesses with coordinates: {with_coords_total:,}")
    logger.info(f"  Businesses with street address: {with_street:,}")
    logger.info(f"  Businesses with phone: {with_phone:,}")
    
    conn.close()

def main():
    """Main update process"""
    start_time = datetime.now()
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / 'input'
    data_dir = project_root / 'backend' / 'data'
    
    jsonl_path = input_dir / 'berlin_business_data.jsonl'
    db_path = data_dir / 'berlin_businesses.db'
    
    logger.info("="*60)
    logger.info("Berlin Business Data Update")
    logger.info("="*60)
    logger.info(f"Input file: {jsonl_path}")
    logger.info(f"Database: {db_path}")
    
    try:
        # Load precise data
        data_map = load_precise_data(jsonl_path)
        
        # Update database
        update_database(db_path, data_map)
        
        # Summary
        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "="*60)
        logger.info("UPDATE COMPLETE!")
        logger.info("="*60)
        logger.info(f"Execution time: {elapsed_time:.2f} seconds")
        logger.info(f"Processing speed: {len(data_map) / elapsed_time:.0f} records/sec")
        logger.info("\nLog file created: data_update.log")
        
        return 0
    
    except Exception as e:
        logger.error(f"FATAL ERROR: Update failed - {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

