"""
Add geocoding (lat/lon) to Berlin businesses using simplified postal code mapping
Uses approximate center points for Berlin postal code areas
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('geocoding.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Simplified Berlin postal code to approximate lat/lon mapping
# These are approximate center points for each postal code area
BERLIN_PLZ_COORDS = {
    # Berlin Mitte
    '10115': (52.5308, 13.3847), '10117': (52.5234, 13.3889), '10119': (52.5302, 13.4047),
    '10178': (52.5200, 13.4050), '10179': (52.5136, 13.4197),
    
    # Prenzlauer Berg
    '10405': (52.5312, 13.4120), '10407': (52.5356, 13.4211), '10409': (52.5394, 13.4266),
    '10435': (52.5437, 13.4113), '10437': (52.5494, 13.4169), '10439': (52.5536, 13.4245),
    
    # Friedrichshain
    '10243': (52.5106, 13.4617), '10245': (52.5014, 13.4697), '10247': (52.5147, 13.4664),
    '10249': (52.5242, 13.4564),
    
    # Kreuzberg  
    '10961': (52.4951, 13.3856), '10963': (52.4968, 13.4046), '10965': (52.4895, 13.3985),
    '10967': (52.4933, 13.4224), '10969': (52.5028, 13.4176),
    
    # Charlottenburg
    '10585': (52.5170, 13.3110), '10587': (52.5226, 13.3264), '10589': (52.5331, 13.3127),
    '10623': (52.5071, 13.3205), '10625': (52.5149, 13.2974), '10627': (52.5096, 13.3041),
    '10629': (52.5166, 13.3106), '10707': (52.4981, 13.2903), '10709': (52.4941, 13.2847),
    '10711': (52.4869, 13.2926), '10713': (52.4831, 13.3134), '10715': (52.4768, 13.3247),
    '10717': (52.4941, 13.3254), '10719': (52.4951, 13.2994),
    
    # Wilmersdorf
    '10777': (52.4961, 13.3457), '10779': (52.4998, 13.3351), '10781': (52.5057, 13.3497),
    '10783': (52.5037, 13.3677), '10785': (52.5088, 13.3746), '10787': (52.5097, 13.3603),
    '10789': (52.5018, 13.3286),
    
    # Schöneberg
    '10823': (52.4858, 13.3544), '10825': (52.4791, 13.3503), '10827': (52.4852, 13.3432),
    '10829': (52.4779, 13.3424), '12101': (52.4768, 13.3663), '12103': (52.4645, 13.3576),
    '12105': (52.4543, 13.3607), '12109': (52.4588, 13.3764),
    
    # Tempelhof
    '12107': (52.4719, 13.3858), '12157': (52.4678, 13.3377), '12159': (52.4592, 13.3427),
    '12161': (52.4531, 13.3318), '12163': (52.4478, 13.3421), '12165': (52.4428, 13.3531),
    '12167': (52.4557, 13.3234), '12169': (52.4447, 13.3319), '12247': (52.4394, 13.3639),
    '12249': (52.4354, 13.3479),
    
    # Neukölln
    '12043': (52.4836, 13.4379), '12045': (52.4746, 13.4303), '12047': (52.4681, 13.4230),
    '12049': (52.4609, 13.4335), '12051': (52.4562, 13.4508), '12053': (52.4541, 13.4393),
    '12055': (52.4436, 13.4294), '12057': (52.4377, 13.4214), '12059': (52.4316, 13.4410),
    '12099': (52.4697, 13.3988),
    
    # Treptow
    '12435': (52.4918, 13.4958), '12437': (52.4852, 13.5197), '12439': (52.4754, 13.5334),
    '12459': (52.4634, 13.5273), '12487': (52.4543, 13.5382), '12489': (52.4443, 13.5485),
    
    # Köpenick
    '12555': (52.4463, 13.5742), '12557': (52.4369, 13.5952), '12559': (52.4281, 13.6153),
    '12587': (52.4377, 13.6383), '12589': (52.4273, 13.6584),
    
    # Lichtenberg
    '10315': (52.5125, 13.4962), '10317': (52.5014, 13.5157), '10318': (52.4854, 13.5352),
    '10319': (52.4987, 13.4987), '10365': (52.5219, 13.4797), '10367': (52.5327, 13.4943),
    '10369': (52.5421, 13.5127),
    
    # Marzahn-Hellersdorf
    '12619': (52.5359, 13.5824), '12621': (52.5447, 13.5964), '12623': (52.5534, 13.6104),
    '12627': (52.5422, 13.6247), '12629': (52.5315, 13.6387), '12679': (52.5489, 13.5547),
    '12681': (52.5387, 13.5687), '12683': (52.5285, 13.5827), '12685': (52.5183, 13.5967),
    '12687': (52.5081, 13.6107), '12689': (52.5512, 13.6447),
    
    # Pankow
    '13051': (52.5672, 13.4538), '13053': (52.5770, 13.4678), '13055': (52.5868, 13.4818),
    '13057': (52.5966, 13.4958), '13059': (52.6064, 13.5098),
    
    # Reinickendorf
    '13403': (52.5893, 13.3324), '13405': (52.5991, 13.3464), '13407': (52.6089, 13.3604),
    '13409': (52.6187, 13.3744), '13435': (52.6002, 13.2984), '13437': (52.6100, 13.3124),
    '13439': (52.6198, 13.3264), '13465': (52.6213, 13.2924), '13467': (52.6311, 13.3064),
    '13469': (52.6409, 13.3204),
    
    # Spandau
    '13581': (52.5342, 13.1982), '13583': (52.5440, 13.2122), '13585': (52.5538, 13.2262),
    '13587': (52.5636, 13.2402), '13589': (52.5734, 13.2542), '13591': (52.5832, 13.2682),
    '13593': (52.5930, 13.2822), '13595': (52.6028, 13.2962), '13597': (52.6126, 13.3102),
    '13599': (52.5448, 13.1842),
    
    # Steglitz
    '12163': (52.4478, 13.3421), '12165': (52.4428, 13.3531), '12167': (52.4557, 13.3234),
    '12169': (52.4447, 13.3319), '12203': (52.4487, 13.3024), '12205': (52.4385, 13.2924),
    '12207': (52.4283, 13.2824), '12209': (52.4181, 13.2724),
    
    # Zehlendorf
    '14129': (52.4298, 13.2264), '14163': (52.4196, 13.2164), '14165': (52.4094, 13.2064),
    '14167': (52.3992, 13.1964), '14169': (52.3890, 13.1864), '14193': (52.4504, 13.2624),
    '14195': (52.4402, 13.2524), '14197': (52.4300, 13.2424), '14199': (52.4198, 13.2324),
}

# Brandenburg postal codes near Berlin (suburbs)
BRANDENBURG_NEAR_BERLIN = {
    # Potsdam
    '14467': (52.3989, 13.0642), '14469': (52.4087, 13.0782), '14471': (52.4185, 13.0922),
    '14473': (52.4283, 13.1062), '14476': (52.4094, 13.0502), '14478': (52.3996, 13.0362),
    '14480': (52.3898, 13.0222), '14482': (52.3800, 13.0082),
    
    # Surrounding areas
    '12529': (52.3849, 13.5202), '14532': (52.3951, 13.2064), '14612': (52.5612, 13.0962),
    '14624': (52.5314, 13.0862), '14641': (52.6082, 13.0762), '14669': (52.5374, 13.0342),
    '15834': (52.3447, 13.4024), '15827': (52.3345, 13.3924), '14974': (52.2947, 13.2624),
}

# Combine all postal codes
ALL_PLZ_COORDS = {**BERLIN_PLZ_COORDS, **BRANDENBURG_NEAR_BERLIN}

def create_plz_lookup():
    """Create lookup dictionary from hardcoded postal codes"""
    logger.info(f"Using built-in postal code database with {len(ALL_PLZ_COORDS)} entries")
    return ALL_PLZ_COORDS

def add_geocoding(businesses, plz_lookup):
    """Add lat/lon coordinates to businesses"""
    logger.info(f"Adding geocoding to {len(businesses):,} businesses...")
    
    geocoded_count = 0
    missing_count = 0
    missing_postcodes = set()
    
    for i, business in enumerate(businesses):
        postal_code = business.get('postal_code', '')
        
        if postal_code in plz_lookup:
            coords = plz_lookup[postal_code]
            business['lat'] = coords[0]
            business['lon'] = coords[1]
            geocoded_count += 1
        else:
            business['lat'] = None
            business['lon'] = None
            missing_count += 1
            missing_postcodes.add(postal_code)
        
        # Progress logging
        if (i + 1) % 10000 == 0:
            logger.info(f"Progress: {i + 1:,}/{len(businesses):,} businesses processed...")
    
    logger.info("="*60)
    logger.info(f"Geocoding complete!")
    logger.info(f"  Successfully geocoded: {geocoded_count:,}")
    logger.info(f"  Missing coordinates: {missing_count:,}")
    logger.info(f"  Success rate: {geocoded_count / len(businesses) * 100:.1f}%")
    
    if missing_postcodes:
        logger.warning(f"  Unique missing postal codes: {len(missing_postcodes)}")
        logger.debug(f"  Missing postcodes: {sorted(missing_postcodes)[:20]}")
    
    logger.info("="*60)
    
    return businesses

def save_geocoded_data(businesses, output_path):
    """Save geocoded data to JSON file"""
    logger.info(f"Saving geocoded data to {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
        
        file_size = output_path.stat().st_size / (1024 * 1024)
        logger.info(f"Data saved successfully! File size: {file_size:.2f} MB")
    
    except Exception as e:
        logger.error(f"Failed to save data: {e}", exc_info=True)
        raise

def main():
    """Main geocoding process"""
    start_time = datetime.now()
    
    # Define paths
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'backend' / 'data'
    
    input_path = data_dir / 'berlin_businesses.json'
    output_path = data_dir / 'berlin_businesses_geocoded.json'
    
    logger.info("="*60)
    logger.info("Berlin Business Geocoding")
    logger.info("="*60)
    logger.info(f"Input file: {input_path}")
    logger.info(f"Output file: {output_path}")
    
    try:
        # Load businesses
        logger.info("Loading Berlin businesses...")
        with open(input_path, 'r', encoding='utf-8') as f:
            businesses = json.load(f)
        logger.info(f"Loaded {len(businesses):,} businesses")
        
        # Create postal code lookup
        plz_lookup = create_plz_lookup()
        
        # Add geocoding
        geocoded_businesses = add_geocoding(businesses, plz_lookup)
        
        # Save results
        save_geocoded_data(geocoded_businesses, output_path)
        
        # Summary
        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "="*60)
        logger.info("GEOCODING COMPLETE!")
        logger.info("="*60)
        logger.info(f"Execution time: {elapsed_time:.2f} seconds")
        logger.info(f"Output file: {output_path}")
        
        # Sample with coordinates
        logger.info("\nSample geocoded businesses:")
        samples_with_coords = [b for b in geocoded_businesses if b.get('lat') and b.get('lon')][:3]
        for i, sample in enumerate(samples_with_coords, 1):
            logger.info(f"\n  Sample {i}:")
            logger.info(f"    Name: {sample['name']}")
            logger.info(f"    City: {sample['city']}")
            logger.info(f"    Postal Code: {sample['postal_code']}")
            logger.info(f"    Coordinates: {sample['lat']:.6f}, {sample['lon']:.6f}")
            categories_str = ', '.join(sample['categories'][:2]) if sample['categories'] else 'None'
            logger.info(f"    Categories: {categories_str}")
        
        logger.info("\nLog file created: geocoding.log")
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"FATAL ERROR: Geocoding failed - {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
