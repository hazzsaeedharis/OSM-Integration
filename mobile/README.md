# 📱 Berlin Business Finder - Mobile App

React Native mobile application for iOS and Android.

## 🚀 Quick Start

### Prerequisites

- ✅ Node.js installed (you have this)
- ✅ Android Studio installed (you have this)
- ✅ React Native CLI installed: `npm install -g react-native-cli`
- ⚠️ **ANDROID_HOME environment variable** (see setup below)

---

## ⚙️ ANDROID_HOME Setup (Required!)

### Step 1: Find Your Android SDK Location

**Default location:**
```
C:\Users\YourUsername\AppData\Local\Android\Sdk
```

**To find it in Android Studio:**
1. Open Android Studio
2. Go to: **File** → **Settings** (or **Configure** → **Settings**)
3. Navigate to: **Appearance & Behavior** → **System Settings** → **Android SDK**
4. Copy the **"Android SDK Location"** path

---

### Step 2: Set Environment Variables

**For Windows:**

1. Press `Win + X` → Select **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under **User variables**, click **New**:
   - **Variable name**: `ANDROID_HOME`
   - **Variable value**: `C:\Users\YourUsername\AppData\Local\Android\Sdk`
5. Find **Path** variable, click **Edit**, add:
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\tools`
   - `%ANDROID_HOME%\tools\bin`
6. Click **OK** on all windows
7. **Restart PowerShell/Command Prompt**

---

### Step 3: Verify Installation

```bash
# Check if Android SDK is accessible
adb version

# Should show: Android Debug Bridge version X.X.X
```

---

## 📦 Installation

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. Install iOS Pods (Mac only)

```bash
cd ios
pod install
cd ..
```

---

## 🎯 Running the App

### Option 1: Android

```bash
# Make sure Android Studio is open OR Android emulator is running
# Then run:
cd mobile
npx react-native run-android
```

**First run will take 5-10 minutes** to build.

### Option 2: Start Metro Bundler Separately

```bash
# Terminal 1: Start Metro
cd mobile
npx react-native start

# Terminal 2: Run Android
npx react-native run-android
```

---

## 🔧 Troubleshooting

### Error: "ANDROID_HOME is not set"

**Solution:**
- Follow the **ANDROID_HOME Setup** section above
- Restart your terminal after setting variables
- Verify with: `echo $env:ANDROID_HOME` (PowerShell)

### Error: "SDK location not found"

**Solution:**
1. Open Android Studio
2. Install Android SDK Platform 33 (or latest)
3. Install Android SDK Build-Tools
4. Restart terminal

### Error: "adb not found"

**Solution:**
- Add platform-tools to PATH: `%ANDROID_HOME%\platform-tools`
- Restart terminal

### Error: "Unable to load script"

**Solution:**
```bash
# Clear cache and restart
npx react-native start --reset-cache
```

### App crashes on startup

**Solution:**
```bash
# Rebuild the app
cd android
gradlew clean
cd ..
npx react-native run-android
```

---

## 📡 Backend API (Required!)

The mobile app needs the FastAPI backend running:

```bash
# Terminal 1: Run FastAPI backend
cd backend/api
py main.py

# API runs on: http://localhost:8000
```

**Make sure the API is running before starting the mobile app!**

---

## 🎨 Features

- ✅ Interactive map with OpenStreetMap
- ✅ Business markers (tap to see details)
- ✅ Search by business name
- ✅ Filter by category and city
- ✅ Language toggle (English/German)
- ✅ Get Directions (opens device maps app)
- ✅ Search on Google
- ✅ Yellow Gelbe Seiten theme
- ✅ Tab navigation (Map, Search, Settings)

---

## 📱 App Structure

```
mobile/
├── src/
│   ├── screens/
│   │   ├── MapScreen.tsx           - Main map view with markers
│   │   ├── SearchScreen.tsx        - Search and filter interface
│   │   ├── SettingsScreen.tsx      - Language and settings
│   │   └── BusinessDetailScreen.tsx - Business details
│   ├── navigation/
│   │   └── AppNavigator.tsx        - Tab and stack navigation
│   ├── services/
│   │   └── api.ts                  - API client (connects to FastAPI)
│   ├── i18n/
│   │   ├── en.json                 - English translations
│   │   ├── de.json                 - German translations
│   │   └── config.ts               - i18n configuration
│   └── theme/
│       └── colors.ts               - App colors (yellow theme)
├── App.tsx                         - Root component
└── package.json                    - Dependencies
```

---

## 🧪 Testing on Android

### 1. Start Android Emulator

**Option A: From Android Studio**
- Open Android Studio
- Click **AVD Manager** (phone icon)
- Click **▶ Play** on an emulator

**Option B: From Command Line**
```bash
emulator -list-avds
emulator -avd YourDeviceName
```

### 2. Install App on Emulator

```bash
cd mobile
npx react-native run-android
```

### 3. Test Features

- ✅ Map loads with Berlin view
- ✅ Search for "Restaurant"
- ✅ Tap markers to see popups
- ✅ Switch to Search tab
- ✅ Apply filters
- ✅ Go to Settings → Toggle language
- ✅ Click "Get Directions"

---

## 🐛 Common Issues

### "Unable to connect to dev server"

**Solution:**
```bash
# Enable adb reverse
adb reverse tcp:8081 tcp:8081
adb reverse tcp:8000 tcp:8000
```

### "Cannot find module" errors

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npx react-native start --reset-cache
```

### Map not showing

**Solution:**
- Make sure Google Play Services is installed on emulator
- Use an emulator with Play Store support

---

## 📊 API Configuration

The app connects to: `http://localhost:8000/api/v1`

**To change API URL** (for production):
Edit `mobile/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://your-api.com/api/v1';
```

---

## 🎉 You're Ready!

Once ANDROID_HOME is set up:

```bash
# Terminal 1: Start API
cd backend/api
py main.py

# Terminal 2: Start Mobile App
cd mobile
npx react-native run-android
```

**Enjoy your mobile app!** 📱
