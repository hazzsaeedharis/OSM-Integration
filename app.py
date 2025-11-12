"""
Berlin Business Finder - Streamlit App
OpenStreetMap Integration with Gelbe Seiten data
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import sqlite3
import json
from pathlib import Path
import pandas as pd
from folium.plugins import Fullscreen

# Page configuration
st.set_page_config(
    page_title="Berlin Business Finder",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Translation dictionary
TRANSLATIONS = {
    'en': {
        'title': '🗺️ Berlin Business Finder',
        'subtitle': 'Find local businesses on OpenStreetMap',
        'search_filters': '🔍 Search & Filters',
        'businesses': 'Businesses',
        'with_coordinates': 'With Coordinates',
        'business_name': 'Business Name',
        'search_placeholder': 'e.g. Hairdresser, Restaurant...',
        'category': 'Category',
        'all': 'All',
        'city_district': 'City/District',
        'max_results': 'Max Results',
        'search_button': '🔍 Search',
        'hints': '💡 Hints',
        'hint_zoom': '**Zoom map**: Mouse wheel or +/- buttons',
        'hint_marker': '**Click marker**: Show details',
        'hint_pan': '**Pan map**: Drag & Drop',
        'map_title': '📍 Map',
        'results_title': '📋 Results',
        'searching': 'Searching businesses...',
        'showing_businesses': '📊 Showing {count} businesses on map',
        'no_results': 'No businesses found. Please adjust your search criteria.',
        'more_businesses': '+ {count} more businesses on map',
        'search_prompt': 'Use the search filters on the left to find businesses.',
        'footer_data': 'Data from Gelbe Seiten | Maps © OpenStreetMap',
        'footer_version': 'Berlin Business Finder v1.0',
        'language': '🌐 Language',
        'fullscreen_map': '🔍 View Fullscreen Map',
        'exit_fullscreen': '❌ Exit Fullscreen',
    },
    'de': {
        'title': '🗺️ Berlin Business Finder',
        'subtitle': 'Finden Sie lokale Unternehmen auf OpenStreetMap',
        'search_filters': '🔍 Suche & Filter',
        'businesses': 'Unternehmen',
        'with_coordinates': 'Mit Koordinaten',
        'business_name': 'Unternehmensname',
        'search_placeholder': 'z.B. Friseur, Restaurant...',
        'category': 'Kategorie',
        'all': 'Alle',
        'city_district': 'Stadt/Bezirk',
        'max_results': 'Max. Ergebnisse',
        'search_button': '🔍 Suchen',
        'hints': '💡 Hinweise',
        'hint_zoom': '**Karte zoomen**: Mausrad oder +/- Buttons',
        'hint_marker': '**Marker klicken**: Details anzeigen',
        'hint_pan': '**Karte verschieben**: Drag & Drop',
        'map_title': '📍 Karte',
        'results_title': '📋 Ergebnisse',
        'searching': 'Suche Unternehmen...',
        'showing_businesses': '📊 Zeige {count} Unternehmen auf der Karte',
        'no_results': 'Keine Unternehmen gefunden. Bitte passen Sie Ihre Suchkriterien an.',
        'more_businesses': '+ {count} weitere Unternehmen auf der Karte',
        'search_prompt': 'Nutzen Sie die Suchfilter links, um Unternehmen zu finden.',
        'footer_data': 'Daten aus Gelbe Seiten | Karten von © OpenStreetMap',
        'footer_version': 'Berlin Business Finder v1.0',
        'language': '🌐 Sprache',
        'fullscreen_map': '🔍 Vollbild Karte',
        'exit_fullscreen': '❌ Vollbild beenden',
    }
}

# Initialize session state for language (default English)
if 'language' not in st.session_state:
    st.session_state.language = 'en'

if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

def t(key):
    """Get translation for current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# Custom CSS for Gelbe Seiten-inspired theme
st.markdown("""
<style>
    /* Main theme colors - Gelbe Seiten yellow */
    :root {
        --primary-color: #FFD700;
        --secondary-color: #FFC107;
        --background-color: #FFFACD;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: #333;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #555;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Business card styling */
    .business-card {
        background: white;
        border-left: 4px solid #FFD700;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .business-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .business-name {
        color: #333;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .business-category {
        background: #FFD700;
        color: #333;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .business-location {
        color: #666;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    /* Stats box */
    .stats-box {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFFACD 100%);
        border: 2px solid #FFD700;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #FFFACD;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
        color: #333;
        font-weight: 600;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_database_connection():
    """Create and cache database connection"""
    db_path = Path('backend/data/berlin_businesses.db')
    if not db_path.exists():
        st.error(f"Database not found at {db_path}. Please run the data processing scripts first.")
        st.stop()
    return sqlite3.connect(db_path, check_same_thread=False)

@st.cache_data
def get_statistics():
    """Get database statistics"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute('SELECT key, value FROM statistics')
    for key, value in cursor.fetchall():
        stats[key] = value
    
    return stats

@st.cache_data
def get_all_categories():
    """Get all unique categories"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT categories FROM businesses WHERE categories IS NOT NULL')
    categories_set = set()
    
    for row in cursor.fetchall():
        try:
            cats = json.loads(row[0])
            categories_set.update(cats)
        except:
            pass
    
    return sorted(list(categories_set))

@st.cache_data
def get_all_cities():
    """Get all unique cities"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT city FROM businesses ORDER BY city')
    cities = [row[0] for row in cursor.fetchall() if row[0]]
    
    return cities

def search_businesses(search_term="", category="", city="", limit=100):
    """Search businesses with filters"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT id, name, postal_code, city, lat, lon, categories, 
               street_address, district, phone, email, website
        FROM businesses
        WHERE lat IS NOT NULL
    '''
    params = []
    
    # Add search filter
    if search_term:
        query += ' AND name LIKE ?'
        params.append(f'%{search_term}%')
    
    # Add category filter
    if category:
        query += ' AND categories LIKE ?'
        params.append(f'%{category}%')
    
    # Add city filter
    if city:
        query += ' AND city = ?'
        params.append(city)
    
    query += ' LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    
    businesses = []
    for row in cursor.fetchall():
        businesses.append({
            'id': row[0],
            'name': row[1],
            'postal_code': row[2],
            'city': row[3],
            'lat': row[4],
            'lon': row[5],
            'categories': json.loads(row[6]) if row[6] else [],
            'street_address': row[7],
            'district': row[8],
            'phone': row[9],
            'email': row[10],
            'website': row[11]
        })
    
    return businesses

def create_map(businesses, center_lat=52.5200, center_lon=13.4050, zoom=11):
    """Create Folium map with business markers and fullscreen capability"""
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add fullscreen button
    Fullscreen(
        position='topright',
        title='Enter fullscreen',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Add markers for businesses
    for business in businesses:
        # Create enhanced popup content
        categories_html = ''.join([
            f'<span style="background:#FFD700;padding:4px 10px;border-radius:12px;margin:2px;display:inline-block;font-size:12px;font-weight:600;color:#333;">{cat}</span>'
            for cat in business['categories'][:3]
        ])
        
        # Build full address
        full_address = business.get('street_address', '')
        district = business.get('district', '')
        if full_address and district:
            address_display = f"{full_address}, {business['postal_code']} {business['city']} ({district})"
        elif full_address:
            address_display = f"{full_address}, {business['postal_code']} {business['city']}"
        else:
            address_display = f"{business['postal_code']} {business['city']}"
        
        # Enhanced popup with all available data
        popup_html = f'''
        <div style="width:320px;font-family:Arial,sans-serif;padding:10px;">
            <h3 style="color:#333;margin:0 0 12px 0;font-size:17px;font-weight:700;border-bottom:2px solid #FFD700;padding-bottom:8px;">
                {business['name']}
            </h3>
            
            <div style="margin:10px 0;">
                {categories_html}
            </div>
            
            <div style="background:#f9f9f9;padding:12px;border-radius:8px;margin:10px 0;">
                <p style="color:#666;font-size:13px;margin:4px 0;line-height:1.6;">
                    <strong>📍 Address:</strong><br/>
                    {address_display}
                </p>
                '''
        
        # Add phone if available
        if business.get('phone'):
            popup_html += f'''
                <p style="color:#666;font-size:13px;margin:8px 0 4px 0;line-height:1.6;">
                    <strong>☎️ Phone:</strong><br/>
                    <a href="tel:{business['phone']}" style="color:#2196F3;text-decoration:none;">{business['phone']}</a>
                </p>
            '''
        
        # Add email if available
        if business.get('email'):
            popup_html += f'''
                <p style="color:#666;font-size:13px;margin:8px 0 4px 0;line-height:1.6;">
                    <strong>📧 Email:</strong><br/>
                    <a href="mailto:{business['email']}" style="color:#2196F3;text-decoration:none;">{business['email']}</a>
                </p>
            '''
        
        # Add website if available
        if business.get('website'):
            popup_html += f'''
                <p style="color:#666;font-size:13px;margin:8px 0 4px 0;line-height:1.6;">
                    <strong>🌐 Website:</strong><br/>
                    <a href="{business['website']}" target="_blank" style="color:#2196F3;text-decoration:none;">{business['website']}</a>
                </p>
            '''
        
        popup_html += f'''
            </div>
            
            <div style="margin-top:12px;">
                <a href="https://www.google.com/maps/search/?api=1&query={business['lat']},{business['lon']}" 
                   target="_blank" 
                   style="display:inline-block;background:#FFD700;color:#333;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:600;font-size:12px;margin-right:5px;">
                    🚗 Get Directions
                </a>
                <a href="https://www.google.com/search?q={business['name']}+{business['postal_code']}+{business['city']}" 
                   target="_blank" 
                   style="display:inline-block;background:#FFC107;color:#333;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:600;font-size:12px;">
                    🔍 Search
                </a>
            </div>
        </div>
        '''
        
        # Create tooltip
        tooltip = f"{business['name']} - {business['city']}"
        
        # Add marker
        folium.Marker(
            location=[business['lat'], business['lon']],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=tooltip,
            icon=folium.Icon(color='orange', icon='info-sign')
        ).add_to(m)
    
    return m

# Main app
def main():
    # Language selector in top right (using columns)
    col_header, col_lang = st.columns([6, 1])
    
    with col_lang:
        st.markdown("<div style='padding-top:20px;'>", unsafe_allow_html=True)
        lang_option = st.selectbox(
            t('language'),
            options=['🇬🇧 English', '🇩🇪 Deutsch'],
            index=0 if st.session_state.language == 'en' else 1,
            label_visibility='collapsed'
        )
        
        # Update language in session state
        if '🇬🇧' in lang_option:
            st.session_state.language = 'en'
        else:
            st.session_state.language = 'de'
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_header:
        # Header with translation
        st.markdown(f"""
        <div class="main-header">
            <h1>{t('title')}</h1>
            <p>{t('subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar with translations
    st.sidebar.title(t('search_filters'))
    
    # Statistics in sidebar
    stats = get_statistics()
    total = int(stats.get('total_businesses', 0))
    geocoded = int(stats.get('geocoded_businesses', 0))
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <div class="stat-value">{total:,}</div>
        <div class="stat-label">{t('businesses')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <div class="stat-value">{geocoded:,}</div>
        <div class="stat-label">{t('with_coordinates')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Search input
    search_term = st.sidebar.text_input(
        t('business_name'),
        placeholder=t('search_placeholder')
    )
    
    # Category filter
    all_categories = get_all_categories()
    category = st.sidebar.selectbox(
        t('category'),
        options=[t('all')] + all_categories
    )
    category = "" if category == t('all') else category
    
    # City filter
    all_cities = get_all_cities()
    city = st.sidebar.selectbox(
        t('city_district'),
        options=[t('all')] + all_cities
    )
    city = "" if city == t('all') else city
    
    # Results limit
    limit = st.sidebar.slider(
        t('max_results'),
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )
    
    # Search button
    search_button = st.sidebar.button(t('search_button'), use_container_width=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {t('hints')}")
    st.sidebar.markdown(f"""
    - {t('hint_zoom')}
    - {t('hint_marker')}
    - {t('hint_pan')}
    """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t('map_title'))
        
        # Perform search
        if 'businesses' not in st.session_state or search_button:
            with st.spinner(t('searching')):
                businesses = search_businesses(search_term, category, city, limit)
                st.session_state.businesses = businesses
        else:
            businesses = st.session_state.businesses
        
        # Display map
        if businesses:
            # Calculate center
            if len(businesses) > 0:
                avg_lat = sum(b['lat'] for b in businesses) / len(businesses)
                avg_lon = sum(b['lon'] for b in businesses) / len(businesses)
                zoom = 12 if len(businesses) < 50 else 11
            else:
                avg_lat, avg_lon, zoom = 52.5200, 13.4050, 11
            
            # Create and display map
            m = create_map(businesses, avg_lat, avg_lon, zoom)
            st_folium(m, width=None, height=600)
            
            st.info(t('showing_businesses').format(count=len(businesses)))
        else:
            st.warning(t('no_results'))
            
            # Show default map
            m = folium.Map(
                location=[52.5200, 13.4050],
                zoom_start=11,
                tiles='OpenStreetMap'
            )
            # Add fullscreen to default map too
            Fullscreen(
                position='topright',
                title='Enter fullscreen',
                title_cancel='Exit fullscreen',
                force_separate_button=True
            ).add_to(m)
            st_folium(m, width=None, height=600)
    
    with col2:
        st.subheader(t('results_title'))
        
        if businesses:
            # Display business cards
            for business in businesses[:20]:  # Show first 20 in list
                categories_badges = ''.join([
                    f'<span class="business-category">{cat}</span>'
                    for cat in business['categories'][:3]
                ])
                
                # Build address display
                if business.get('street_address'):
                    location_text = f"{business['street_address']}, {business['postal_code']} {business['city']}"
                    if business.get('district'):
                        location_text += f" ({business['district']})"
                else:
                    location_text = f"{business['postal_code']} {business['city']}"
                
                st.markdown(f"""
                <div class="business-card">
                    <div class="business-name">{business['name']}</div>
                    <div>{categories_badges}</div>
                    <div class="business-location">
                        📍 {location_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(businesses) > 20:
                st.info(t('more_businesses').format(count=len(businesses) - 20))
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:2rem;color:#666;">
                <p style="font-size:3rem;">🔍</p>
                <p>{t('search_prompt')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;color:#666;padding:1rem;">
        <p>{t('footer_data')}</p>
        <p style="font-size:0.85rem;">{t('footer_version')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

