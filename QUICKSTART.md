# 🚀 Quick Start Guide

## Get Started in 3 Minutes!

### Prerequisites
- Python 3.8+ installed
- Data files in `input/` folder ✓ (already present)
- Processed data in `backend/data/` ✓ (already created)

---

## Option 1: Just Run It! (Data Already Processed)

```bash
# 1. Install dependencies (first time only)
py -m pip install -r requirements.txt

# 2. Launch the app
py -m streamlit run app.py
```

**That's it!** The app will open in your browser at `http://localhost:8501`

---

## Option 2: Reprocess Data (Optional)

If you want to reprocess the data from scratch:

```bash
# Step 1: Extract Berlin businesses (2 minutes)
py backend/scripts/extract_berlin_data.py

# Step 2: Add GPS coordinates (1 second)
py backend/scripts/geocode_businesses.py

# Step 3: Create database (2 seconds)
py backend/scripts/create_database.py

# Step 4: Launch app
py -m streamlit run app.py
```

---

## 🎯 First Search

Once the app is running:

1. **Search by name**: Try "Friseur" (hairdresser)
2. **Filter by category**: Select "Friseure" or any category
3. **Filter by district**: Choose "Berlin" or any district
4. **Click markers**: See business details
5. **Hover markers**: Quick preview

---

## 📊 What You Get

- **74,212** Berlin businesses
- **56,898** with GPS coordinates
- **Interactive map** with OpenStreetMap
- **Fast search** with SQLite
- **Yellow theme** inspired by Gelbe Seiten

---

## 🐛 Troubleshooting

### Python not found?
```bash
# Try with py launcher
py --version
```

### Port already in use?
```bash
# Use different port
py -m streamlit run app.py --server.port 8502
```

### Database error?
```bash
# Recreate database
py backend/scripts/create_database.py
```

---

## 💡 Tips

- **Reduce results** if map is slow
- **Use filters** for better results
- **Check logs** if something goes wrong:
  - `extraction.log`
  - `geocoding.log`
  - `database_creation.log`

---

## 📞 Need Help?

- Check `README.md` for full documentation
- Check `PROJECT_SUMMARY.md` for technical details
- Review log files for error messages

---

**Enjoy exploring Berlin businesses! 🗺️**

