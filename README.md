# 🗺️ Berlin Business Finder

An interactive tool for visualizing Berlin businesses on OpenStreetMap with Gelbe Seiten (Yellow Pages) data.

## ✨ Features

- **🗺️ Interactive Map**: OpenStreetMap integration with Folium
- **🔍 Advanced Search**: Filter by name, category, and city/district
- **📍 56,898 Geocoded Businesses**: Out of 74,212 total Berlin businesses
- **💡 Hover Tooltips**: Business information on mouse hover
- **🎨 Gelbe Seiten Design**: Inspired by the original Yellow Pages design
- **⚡ Fast Search**: SQLite database with Full-Text Search
- **📱 Responsive Design**: Works on desktop and tablet

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- The provided data files (`gsbestand-559.json` and `gs_final.json`)

### 1. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### 2. Process Data (Already Done!)

The data processing steps have already been completed:

```bash
# Step 1: Extract Berlin businesses
py backend/scripts/extract_berlin_data.py

# Step 2: Add geocoding
py backend/scripts/geocode_businesses.py

# Step 3: Create SQLite database
py backend/scripts/create_database.py
```

### 3. Launch Streamlit App

```bash
py -m streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📊 Data Statistics

- **Total Businesses**: 74,212
- **With Coordinates**: 56,898 (76.7%)
- **Unique Postal Codes**: 207
- **Unique Cities**: 141
- **Database Size**: 19.85 MB

## 🎯 Usage

### Search for Businesses

1. **Search by Name**: Enter a business name in the search field (e.g., "Friseur")
2. **Filter by Category**: Select a category from the dropdown list
3. **Filter by District**: Choose a Berlin district or city
4. **Max Results**: Adjust the number of displayed businesses

### Map Controls

- **Zoom**: Mouse wheel or +/- buttons
- **Pan**: Drag the map with your mouse
- **Click Markers**: View business details
- **Tooltips**: Hover over markers to see business names

## 📁 Project Structure

```
OSM-Integration/
├── app.py                          # Main application (Streamlit)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── backend/
│   ├── data/
│   │   ├── berlin_businesses.json           # Extracted Berlin data
│   │   ├── berlin_businesses_geocoded.json  # With coordinates
│   │   └── berlin_businesses.db             # SQLite database
│   │
│   └── scripts/
│       ├── extract_berlin_data.py    # Data extraction with logging
│       ├── geocode_businesses.py     # Geocoding with built-in PLZ data
│       └── create_database.py        # Database creation
│
└── input/
    ├── gsbestand-559.json           # Original data (3.8 GB)
    └── gs_final.json                # Categories data
```

## 🛠️ Technology Stack

### Backend & Data Processing
- **Python 3.13**: Programming language
- **SQLite**: Database with Full-Text Search
- **Streaming Processing**: Line-by-line reading for memory efficiency
- **Comprehensive Logging**: All scripts generate detailed log files

### Frontend & Visualization
- **Streamlit**: Web framework (Pure Python!)
- **Folium**: OpenStreetMap integration
- **Pandas**: Data processing

### Data Sources
- **Gelbe Seiten**: Business data
- **OpenStreetMap**: Map tiles

## 📝 Logs

All processing steps generate log files with timestamps and error tracking:

- `extraction.log` - Data extraction (3.4M records processed)
- `geocoding.log` - Geocoding (76.7% success rate)
- `database_creation.log` - Database creation with statistics

## ⚙️ Configuration

### Adjust Number of Markers

In `app.py`, line 239:
```python
limit = st.sidebar.slider(
    "Max. Ergebnisse",
    min_value=10,
    max_value=500,  # Adjust here
    value=100,
    step=10
)
```

### Change Map Center Position

In `app.py`, `create_map()` function:
```python
m = folium.Map(
    location=[52.5200, 13.4050],  # Berlin center
    zoom_start=11,
    tiles='OpenStreetMap'
)
```

## 🎨 Design Customization

The design can be customized through CSS styles in `app.py`. Main colors:

- **Primary Color**: `#FFD700` (Yellow)
- **Secondary Color**: `#FFC107` (Orange-Yellow)
- **Background**: `#FFFACD` (Light-Yellow)

## 📈 Performance

- **Data Extraction**: ~2 minutes for 3.4M entries (streaming)
- **Geocoding**: ~1.2 seconds for 74K businesses
- **Database Creation**: ~2 seconds with FTS indexing
- **Map Rendering**: < 1 second for 100 markers

## 🐛 Troubleshooting

### Database Not Found

```bash
# Recreate database
py backend/scripts/create_database.py
```

### Port Already in Use

```bash
# Use different port
py -m streamlit run app.py --server.port 8502
```

### Too Many Markers Slow Down Map

Reduce "Max Results" in the sidebar or refine search criteria.

### Python/Pip Not Recognized

```bash
# Use py launcher
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## 🔮 Future Enhancements

Potential improvements:

1. **Full Dataset**: Integration of all German businesses (3.4M)
2. **Marker Clustering**: Better performance with many markers
3. **Detail Pages**: Complete business information with contact details
4. **Route Planning**: Navigation features
5. **Export**: Export search results as CSV/Excel
6. **REST API**: API for external applications
7. **User Accounts**: Save favorites and notes

## 📄 License

This project uses data from Gelbe Seiten and OpenStreetMap.

## 👨‍💻 Author

Created as an OSM-Integration project for cost reduction and improved data visualization.

## 🙏 Acknowledgments

- **OpenStreetMap Contributors**: For the free map data
- **Gelbe Seiten**: For the business data
- **Streamlit & Folium**: For the great Python libraries

---

# 🇩🇪 Deutsche Version

## Über das Projekt

Ein interaktives Tool zur Visualisierung von Berliner Unternehmen auf OpenStreetMap mit Gelbe Seiten Daten.

## Features

- **Interaktive Karte** mit 56.898 geokodierten Unternehmen
- **Erweiterte Suchfunktion** nach Name, Kategorie und Bezirk
- **Gelbe Seiten Design** mit gelbem Theme
- **Schnelle SQLite-Datenbank** mit Volltextsuche
- **Reine Python-Implementierung** - kein JavaScript erforderlich!

## Installation

```bash
# Abhängigkeiten installieren
py -m pip install -r requirements.txt

# App starten
py -m streamlit run app.py
```

## Verwendung

1. Öffnen Sie `http://localhost:8501` in Ihrem Browser
2. Nutzen Sie die Suchfilter in der Seitenleiste
3. Klicken Sie auf Marker für Details
4. Zoomen und verschieben Sie die Karte nach Bedarf

## Datenverarbeitung

Alle Skripte verwenden **Streaming** und **umfassendes Logging**:

```bash
# Berlin-Daten extrahieren (74.212 Unternehmen)
py backend/scripts/extract_berlin_data.py

# Koordinaten hinzufügen (76.7% Erfolgsrate)
py backend/scripts/geocode_businesses.py

# Datenbank erstellen (19.85 MB)
py backend/scripts/create_database.py
```

## Technische Details

- **Streaming-Verarbeitung**: Zeile für Zeile für Speichereffizienz
- **Logging**: Alle Fehler und Fortschritte werden protokolliert
- **Keine JavaScript-Kenntnisse** erforderlich - alles in Python!
- **SQLite mit FTS**: Schnelle Volltextsuche
- **153 Postleitzahlen** mit eingebauter Geokodierung

## Support

Bei Fragen oder Problemen überprüfen Sie die Log-Dateien:
- `extraction.log`
- `geocoding.log`
- `database_creation.log`
