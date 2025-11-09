"""
Extract Berlin businesses from Gelbe Seiten data
Merges gsbestand and gs_final data to create a clean dataset
"""

import json
import re
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Berlin and surrounding Brandenburg postal codes
BERLIN_POSTAL_CODES = set(range(10115, 14200))  # Berlin: 10xxx-14xxx

def is_berlin_business(postal_code):
    """Check if postal code is in Berlin area"""
    try:
        plz = int(postal_code)
        return plz in BERLIN_POSTAL_CODES
    except (ValueError, TypeError):
        logger.debug(f"Invalid postal code format: {postal_code}")
        return False

def extract_business_name(person_liste):
    """Extract business name from personListe"""
    if person_liste and len(person_liste) > 0:
        return person_liste[0].get('name', '').strip()
    return ''

def load_categories_map(gs_final_path):
    """Load category mappings from gs_final.json"""
    logger.info(f"Loading category mappings from {gs_final_path}...")
    
    try:
        with open(gs_final_path, 'r', encoding='utf-8') as f:
            gs_final_data = json.load(f)
        
        logger.info(f"Successfully loaded {len(gs_final_data)} entries from gs_final.json")
        
        # Create mapping: business_name -> categories
        categories_map = {}
        for entry in gs_final_data:
            business_name = entry.get('business_name', '').strip()
            categories = entry.get('categories', [])
            if business_name and categories:
                # Extract category text from categories list
                category_texts = [cat.get('text', '') for cat in categories if cat.get('text')]
                categories_map[business_name] = category_texts
        
        logger.info(f"Created mapping for {len(categories_map)} businesses with categories")
        return categories_map
    
    except FileNotFoundError:
        logger.error(f"File not found: {gs_final_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in gs_final.json: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading categories: {e}", exc_info=True)
        raise

def extract_berlin_businesses(gsbestand_path, categories_map):
    """Extract Berlin businesses from gsbestand file - streaming line by line"""
    logger.info(f"Starting extraction from {gsbestand_path}")
    logger.info("Using streaming line-by-line processing for memory efficiency")
    
    berlin_businesses = []
    total_count = 0
    berlin_count = 0
    json_errors = 0
    processing_errors = 0
    
    try:
        with open(gsbestand_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total_count += 1
                
                # Progress logging every 100k records
                if total_count % 100000 == 0:
                    logger.info(f"Progress: {total_count:,} records processed, {berlin_count:,} Berlin businesses found")
                
                try:
                    record = json.loads(line.strip())
                    
                    # Extract address information
                    verlagsdaten = record.get('verlagsdaten', {})
                    kontakt = verlagsdaten.get('kontaktinformationen', {})
                    adresse = kontakt.get('adresse', {})
                    
                    postal_code = adresse.get('postleitzahl', '')
                    city = adresse.get('ortsname', '')
                    
                    # Check if Berlin business
                    if not is_berlin_business(postal_code):
                        continue
                    
                    # Extract business name
                    person_liste = kontakt.get('personListe', [])
                    business_name = extract_business_name(person_liste)
                    
                    if not business_name:
                        logger.debug(f"Line {line_num}: No business name found, skipping")
                        continue
                    
                    # Get categories from mapping
                    categories = categories_map.get(business_name, [])
                    
                    # Extract branch IDs as fallback
                    branch_ids = verlagsdaten.get('branchenIdListe', [])
                    
                    business = {
                        'id': record.get('_id', ''),
                        'name': business_name,
                        'postal_code': postal_code,
                        'city': city,
                        'categories': categories,
                        'branch_ids': branch_ids
                    }
                    
                    berlin_businesses.append(business)
                    berlin_count += 1
                    
                except json.JSONDecodeError as e:
                    json_errors += 1
                    logger.debug(f"Line {line_num}: JSON decode error - {e}")
                    continue
                except KeyError as e:
                    processing_errors += 1
                    logger.debug(f"Line {line_num}: Missing key - {e}")
                    continue
                except Exception as e:
                    processing_errors += 1
                    logger.warning(f"Line {line_num}: Unexpected error - {e}")
                    continue
        
        # Final summary
        logger.info("="*60)
        logger.info(f"Extraction completed successfully!")
        logger.info(f"Total records processed: {total_count:,}")
        logger.info(f"Berlin businesses found: {berlin_count:,}")
        logger.info(f"JSON decode errors: {json_errors}")
        logger.info(f"Processing errors: {processing_errors}")
        logger.info("="*60)
        
        return berlin_businesses
    
    except FileNotFoundError:
        logger.error(f"File not found: {gsbestand_path}")
        raise
    except Exception as e:
        logger.error(f"Critical error during extraction: {e}", exc_info=True)
        raise

def save_berlin_data(businesses, output_path):
    """Save extracted data to JSON file"""
    logger.info(f"Saving {len(businesses):,} businesses to {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
        
        # Get file size for logging
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"Data saved successfully! File size: {file_size:.2f} MB")
        
    except IOError as e:
        logger.error(f"Failed to write file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving data: {e}", exc_info=True)
        raise

def main():
    """Main extraction process"""
    start_time = datetime.now()
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / 'input'
    output_dir = project_root / 'backend' / 'data'
    output_dir.mkdir(exist_ok=True)
    
    gsbestand_path = input_dir / 'gsbestand-559.json'
    gs_final_path = input_dir / 'gs_final.json'
    output_path = output_dir / 'berlin_businesses.json'
    
    logger.info("="*60)
    logger.info("Berlin Business Data Extraction")
    logger.info("="*60)
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    
    try:
        # Load category mappings
        categories_map = load_categories_map(gs_final_path)
        
        # Extract Berlin businesses
        berlin_businesses = extract_berlin_businesses(gsbestand_path, categories_map)
        
        # Save to file
        save_berlin_data(berlin_businesses, output_path)
        
        # Calculate statistics
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        logger.info("\n" + "="*60)
        logger.info("EXTRACTION COMPLETE!")
        logger.info("="*60)
        logger.info(f"Output file: {output_path}")
        logger.info(f"Execution time: {elapsed_time:.2f} seconds")
        logger.info(f"Processing speed: {len(berlin_businesses) / elapsed_time:.0f} businesses/sec")
        
        # Print sample businesses
        if berlin_businesses:
            logger.info("\nSample businesses:")
            for i, sample in enumerate(berlin_businesses[:3], 1):
                logger.info(f"\n  Sample {i}:")
                logger.info(f"    Name: {sample['name']}")
                logger.info(f"    City: {sample['city']}")
                logger.info(f"    Postal Code: {sample['postal_code']}")
                categories_str = ', '.join(sample['categories'][:3]) if sample['categories'] else 'None'
                logger.info(f"    Categories: {categories_str}")
        
        logger.info("\nLog file created: extraction.log")
        return 0
        
    except Exception as e:
        logger.error(f"FATAL ERROR: Extraction failed - {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

