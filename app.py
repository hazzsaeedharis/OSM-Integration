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

# Page configuration
st.set_page_config(
    page_title="Berlin Business Finder",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        SELECT id, name, postal_code, city, lat, lon, categories
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
            'categories': json.loads(row[6]) if row[6] else []
        })
    
    return businesses

def create_map(businesses, center_lat=52.5200, center_lon=13.4050, zoom=11):
    """Create Folium map with business markers"""
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add markers for businesses
    for business in businesses:
        # Create popup content
        categories_html = ''.join([
            f'<span style="background:#FFD700;padding:2px 8px;border-radius:10px;margin:2px;display:inline-block;font-size:11px;">{cat}</span>'
            for cat in business['categories'][:3]
        ])
        
        popup_html = f'''
        <div style="width:250px;font-family:Arial,sans-serif;">
            <h4 style="color:#333;margin:0 0 8px 0;font-size:14px;">{business['name']}</h4>
            <div style="margin:8px 0;">{categories_html}</div>
            <p style="color:#666;font-size:12px;margin:4px 0;">
                📍 {business['postal_code']} {business['city']}
            </p>
        </div>
        '''
        
        # Create tooltip
        tooltip = business['name']
        
        # Add marker
        folium.Marker(
            location=[business['lat'], business['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=tooltip,
            icon=folium.Icon(color='orange', icon='info-sign')
        ).add_to(m)
    
    return m

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🗺️ Berlin Business Finder</h1>
        <p>Finden Sie lokale Unternehmen auf OpenStreetMap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔍 Suche & Filter")
    
    # Statistics in sidebar
    stats = get_statistics()
    total = int(stats.get('total_businesses', 0))
    geocoded = int(stats.get('geocoded_businesses', 0))
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <div class="stat-value">{total:,}</div>
        <div class="stat-label">Unternehmen</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <div class="stat-value">{geocoded:,}</div>
        <div class="stat-label">Mit Koordinaten</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Search input
    search_term = st.sidebar.text_input(
        "Unternehmensname",
        placeholder="z.B. Friseur, Restaurant..."
    )
    
    # Category filter
    all_categories = get_all_categories()
    category = st.sidebar.selectbox(
        "Kategorie",
        options=["Alle"] + all_categories
    )
    category = "" if category == "Alle" else category
    
    # City filter
    all_cities = get_all_cities()
    city = st.sidebar.selectbox(
        "Stadt/Bezirk",
        options=["Alle"] + all_cities
    )
    city = "" if city == "Alle" else city
    
    # Results limit
    limit = st.sidebar.slider(
        "Max. Ergebnisse",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )
    
    # Search button
    search_button = st.sidebar.button("🔍 Suchen", use_container_width=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Hinweise")
    st.sidebar.markdown("""
    - **Karte zoomen**: Mausrad oder +/- Buttons
    - **Marker klicken**: Details anzeigen
    - **Karte verschieben**: Drag & Drop
    """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 Karte")
        
        # Perform search
        if 'businesses' not in st.session_state or search_button:
            with st.spinner('Suche Unternehmen...'):
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
            
            st.info(f"📊 Zeige {len(businesses)} Unternehmen auf der Karte")
        else:
            st.warning("Keine Unternehmen gefunden. Bitte passen Sie Ihre Suchkriterien an.")
            
            # Show default map
            m = folium.Map(
                location=[52.5200, 13.4050],
                zoom_start=11,
                tiles='OpenStreetMap'
            )
            st_folium(m, width=None, height=600)
    
    with col2:
        st.subheader("📋 Ergebnisse")
        
        if businesses:
            # Display business cards
            for business in businesses[:20]:  # Show first 20 in list
                categories_badges = ''.join([
                    f'<span class="business-category">{cat}</span>'
                    for cat in business['categories'][:3]
                ])
                
                st.markdown(f"""
                <div class="business-card">
                    <div class="business-name">{business['name']}</div>
                    <div>{categories_badges}</div>
                    <div class="business-location">
                        📍 {business['postal_code']} {business['city']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(businesses) > 20:
                st.info(f"+ {len(businesses) - 20} weitere Unternehmen auf der Karte")
        else:
            st.markdown("""
            <div style="text-align:center;padding:2rem;color:#666;">
                <p style="font-size:3rem;">🔍</p>
                <p>Nutzen Sie die Suchfilter links, um Unternehmen zu finden.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#666;padding:1rem;">
        <p>Daten aus Gelbe Seiten | Karten von © OpenStreetMap</p>
        <p style="font-size:0.85rem;">Berlin Business Finder v1.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

