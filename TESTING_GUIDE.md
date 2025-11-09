# 🧪 Testing Guide - Berlin Business Finder

## 🚀 How to Run the App

### Step 1: Start the Application

```bash
cd "D:\Desktop\Test_Projects\1.5 Mill Cost reduction\OSM-Integration"
py -m streamlit run app.py
```

The app should automatically open in your browser. If not, manually open:
- **Local URL**: http://localhost:8501
- **Network URL**: Will be shown in terminal

---

## ✅ What You Should See

### 1. **Main Header** (Yellow gradient)
- Title: "🗺️ Berlin Business Finder"
- Subtitle: "Finden Sie lokale Unternehmen auf OpenStreetMap"

### 2. **Sidebar (Left)**
- Search box
- Category dropdown
- City dropdown
- Results slider
- Search button (yellow)
- Statistics boxes showing:
  - 74,212 total businesses
  - 56,898 with coordinates

### 3. **Main Area**
- **Left**: Interactive map (OpenStreetMap)
- **Right**: Business results list

---

## 🧪 Test Cases

### Test 1: Basic Map Loading
**Expected**: 
- ✅ Map loads centered on Berlin (52.52°N, 13.40°E)
- ✅ OpenStreetMap tiles visible
- ✅ Zoom controls (+/-) visible
- ✅ No errors in browser console

**How to Test**:
1. Open app
2. Map should load immediately
3. Try zooming in/out with mouse wheel
4. Try panning by dragging the map

---

### Test 2: Search by Business Name
**Test Input**: `Friseur` (hairdresser)

**Steps**:
1. Enter "Friseur" in the search box (sidebar)
2. Click "🔍 Suchen" button
3. Wait 1-2 seconds

**Expected Results**:
- ✅ Multiple orange markers appear on map
- ✅ Business list shows on right side
- ✅ Info message shows number of results (e.g., "Zeige 100 Unternehmen")
- ✅ Map centers on the results

---

### Test 3: Filter by Category
**Test Input**: Select "Friseure" from category dropdown

**Steps**:
1. Clear search box
2. Select "Friseure" from "Kategorie" dropdown
3. Click "🔍 Suchen"

**Expected Results**:
- ✅ Only hairdresser businesses shown
- ✅ Markers update on map
- ✅ Category badge visible on business cards
- ✅ Results count updates

---

### Test 4: Filter by City/District
**Test Input**: Select "Berlin" from city dropdown

**Steps**:
1. Clear all filters
2. Select "Berlin" from "Stadt/Bezirk" dropdown
3. Click "🔍 Suchen"

**Expected Results**:
- ✅ Only Berlin businesses shown
- ✅ Map zooms to Berlin area
- ✅ Results update

---

### Test 5: Marker Hover Tooltip
**Steps**:
1. Search for any business (e.g., "Restaurant")
2. Hover mouse over any orange marker
3. Don't click, just hover

**Expected Results**:
- ✅ Tooltip appears showing business name
- ✅ Tooltip follows mouse slightly
- ✅ Tooltip disappears when mouse moves away

---

### Test 6: Marker Click Popup
**Steps**:
1. Search for any business
2. Click on an orange marker

**Expected Results**:
- ✅ Popup window opens
- ✅ Shows business name (bold)
- ✅ Shows category badges (yellow background)
- ✅ Shows location (📍 postal code + city)
- ✅ Popup is styled and readable
- ✅ Can close popup by clicking X

---

### Test 7: Combined Filters
**Test Input**: 
- Name: "Auto"
- Category: "Automobile"
- City: "Berlin"

**Steps**:
1. Enter "Auto" in search box
2. Select "Automobile" from category
3. Select "Berlin" from city
4. Click search

**Expected Results**:
- ✅ Only matching businesses shown
- ✅ Fewer results than before
- ✅ All results are relevant
- ✅ Map updates accordingly

---

### Test 8: Results Limit Slider
**Steps**:
1. Search for "Restaurant"
2. Note number of results
3. Adjust "Max. Ergebnisse" slider to 50
4. Click search again

**Expected Results**:
- ✅ Maximum 50 markers on map
- ✅ Info message shows updated count
- ✅ Performance improves with fewer markers

---

### Test 9: Business Cards Display
**Steps**:
1. Search for any business
2. Look at right sidebar

**Expected Results**:
- ✅ Business cards appear in list
- ✅ Each card shows:
  - Business name (bold)
  - Category badges (yellow)
  - Location with 📍 icon
- ✅ Cards have white background
- ✅ Cards have hover effect (slide right slightly)
- ✅ Shows first 20 businesses
- ✅ Message if more than 20 (e.g., "+ 80 weitere Unternehmen")

---

### Test 10: Empty Search
**Steps**:
1. Clear all filters
2. Enter a nonsense search term: "ZZZZXYZ123"
3. Click search

**Expected Results**:
- ✅ Warning message: "Keine Unternehmen gefunden"
- ✅ Empty map shown
- ✅ Helpful suggestion to adjust search
- ✅ No errors in console

---

### Test 11: Statistics Display
**Steps**:
1. Look at sidebar (left)
2. Check statistics boxes

**Expected Results**:
- ✅ First box shows "74,212" (total businesses)
- ✅ Second box shows "56,898" (with coordinates)
- ✅ Boxes have yellow gradient background
- ✅ Numbers are large and readable

---

### Test 12: Responsive Design
**Steps**:
1. Resize browser window
2. Try different widths

**Expected Results**:
- ✅ Map stays responsive
- ✅ Sidebar stays accessible
- ✅ Content doesn't overflow
- ✅ Scrollbars appear if needed

---

### Test 13: Performance Test
**Steps**:
1. Set "Max. Ergebnisse" to 500
2. Search for common term like "GmbH"
3. Wait for map to load

**Expected Results**:
- ✅ Map loads within 2-3 seconds
- ✅ All 500 markers visible
- ✅ No browser freeze
- ✅ Zoom/pan still smooth

---

### Test 14: Map Controls
**Steps**:
1. Test all map interactions:
   - Zoom in (+)
   - Zoom out (-)
   - Mouse wheel zoom
   - Drag to pan
   - Double-click to zoom

**Expected Results**:
- ✅ All controls work smoothly
- ✅ Map stays responsive
- ✅ Markers stay in correct positions
- ✅ No lag or glitches

---

### Test 15: Theme & Styling
**Steps**:
1. Check visual elements

**Expected Results**:
- ✅ Yellow/gold theme throughout (#FFD700, #FFC107)
- ✅ Gradient header at top
- ✅ Yellow category badges
- ✅ Yellow search button
- ✅ Professional, clean appearance
- ✅ Good contrast and readability

---

## 🐛 Common Issues & Solutions

### Issue 1: App Won't Start
**Error**: "Port 8501 already in use"
**Solution**:
```bash
py -m streamlit run app.py --server.port 8502
```

### Issue 2: Database Not Found
**Error**: "Database not found at backend/data/berlin_businesses.db"
**Solution**:
```bash
py backend/scripts/create_database.py
```

### Issue 3: No Markers Visible
**Cause**: No businesses match filters
**Solution**: Try broader search or reset filters

### Issue 4: Map Slow
**Cause**: Too many markers
**Solution**: Reduce "Max. Ergebnisse" to 100 or less

### Issue 5: Import Errors
**Error**: "Module not found"
**Solution**:
```bash
py -m pip install -r requirements.txt
```

---

## 📊 Expected Performance Metrics

| Action | Expected Time |
|--------|---------------|
| Initial page load | < 2 seconds |
| Search query | < 1 second |
| Map render (100 markers) | < 1 second |
| Map render (500 markers) | < 3 seconds |
| Marker click response | Instant |
| Filter change | < 1 second |

---

## ✅ Success Criteria

The app is working correctly if:

1. ✅ Loads without errors
2. ✅ Map displays correctly
3. ✅ Search returns results
4. ✅ Filters work properly
5. ✅ Markers show on map
6. ✅ Tooltips appear on hover
7. ✅ Popups open on click
8. ✅ Business cards display
9. ✅ Statistics show correctly
10. ✅ Yellow theme visible throughout

---

## 📸 Screenshot Checklist

If taking screenshots, capture:

1. **Overview**: Full app with map and sidebar
2. **Search Results**: After searching "Friseur"
3. **Marker Popup**: Clicked marker with business details
4. **Business Cards**: Right sidebar with results
5. **Filters**: Sidebar with dropdowns open
6. **Statistics**: Yellow boxes with numbers

---

## 🎯 Quick Test Sequence (2 minutes)

1. ✅ Open app → Check it loads
2. ✅ Search "Friseur" → Check results appear
3. ✅ Click marker → Check popup opens
4. ✅ Hover marker → Check tooltip works
5. ✅ Change category filter → Check updates
6. ✅ Adjust slider → Check marker count changes

**If all 6 steps work → App is functioning correctly!** 🎉

---

## 🆘 Getting Help

If something doesn't work:

1. Check browser console for errors (F12)
2. Check terminal for Python errors
3. Review log files:
   - `extraction.log`
   - `geocoding.log`
   - `database_creation.log`
4. Verify all files exist in `backend/data/`

---

**Happy Testing! 🧪✨**

