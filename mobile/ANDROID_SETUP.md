# 🤖 Android Setup Guide - Complete Instructions

## 📍 Step-by-Step ANDROID_HOME Configuration

### Step 1: Locate Your Android SDK

#### Option A: Via Android Studio
1. Open **Android Studio**
2. Click **More Actions** → **SDK Manager** (or from top menu: **Tools** → **SDK Manager**)
3. Look at the top: **"Android SDK Location"**
4. Copy this path (example: `C:\Users\h.haris\AppData\Local\Android\Sdk`)

#### Option B: Default Location
The Android SDK is usually at:
```
C:\Users\<YourUsername>\AppData\Local\Android\Sdk
```

Replace `<YourUsername>` with your Windows username.

---

### Step 2: Set ANDROID_HOME Environment Variable

#### Windows 10/11 GUI Method:

1. **Open System Properties:**
   - Press `Win + R`
   - Type: `sysdm.cpl`
   - Press Enter

2. **Go to Environment Variables:**
   - Click **Advanced** tab
   - Click **Environment Variables** button at bottom

3. **Add ANDROID_HOME:**
   - Under **"User variables"** section
   - Click **New**
   - **Variable name:** `ANDROID_HOME`
   - **Variable value:** `C:\Users\h.haris\AppData\Local\Android\Sdk` (your path)
   - Click **OK**

4. **Update PATH:**
   - Still in User variables
   - Find **Path** variable
   - Click **Edit**
   - Click **New** and add these 3 lines:
     ```
     %ANDROID_HOME%\platform-tools
     %ANDROID_HOME%\tools
     %ANDROID_HOME%\tools\bin
     ```
   - Click **OK** on all windows

5. **IMPORTANT: Restart PowerShell**
   - Close all PowerShell/CMD windows
   - Open a new one

#### PowerShell Command Method:

```powershell
# Set ANDROID_HOME (adjust path if needed)
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Users\h.haris\AppData\Local\Android\Sdk", "User")

# Add to PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPaths = @(
    "$env:ANDROID_HOME\platform-tools",
    "$env:ANDROID_HOME\tools",
    "$env:ANDROID_HOME\tools\bin"
)
[Environment]::SetEnvironmentVariable("Path", "$currentPath;$($newPaths -join ';')", "User")

# Restart PowerShell after running this!
```

---

### Step 3: Verify Installation

**Close and reopen PowerShell**, then run:

```powershell
# Check ANDROID_HOME is set
echo $env:ANDROID_HOME
# Should output: C:\Users\h.haris\AppData\Local\Android\Sdk

# Check adb is accessible
adb version
# Should output: Android Debug Bridge version X.X.X

# List connected devices
adb devices
# Should output: List of devices attached
```

---

## 🎯 Required Android SDK Components

Open **Android Studio** → **SDK Manager** → **SDK Platforms** tab:

### Install These:
- ✅ **Android 13 (API Level 33)** - Recommended
- ✅ **Android 12 (API Level 31)**
- ✅ **Android SDK Platform-Tools** (SDK Tools tab)
- ✅ **Android SDK Build-Tools** (SDK Tools tab)
- ✅ **Android Emulator** (SDK Tools tab)

---

## 📱 Create Android Virtual Device (AVD)

### Via Android Studio:

1. **Open AVD Manager:**
   - Click phone icon in toolbar OR
   - **Tools** → **Device Manager**

2. **Create New Device:**
   - Click **Create Device**
   - Select: **Phone** → **Pixel 5** (recommended)
   - Click **Next**

3. **Select System Image:**
   - Choose **R** or **S** (API 31-33)
   - Must have **Google Play** icon (required for maps)
   - Click **Download** if not installed
   - Click **Next**

4. **Finish Setup:**
   - Name: "Pixel_5_API_33"
   - Click **Finish**

5. **Start Emulator:**
   - Click **▶ Play** button
   - Wait for emulator to boot (1-2 minutes)

---

## 🧪 Test Your Setup

### Test 1: Check ANDROID_HOME

```powershell
echo $env:ANDROID_HOME
# Expected: C:\Users\h.haris\AppData\Local\Android\Sdk
```

### Test 2: Check ADB

```powershell
adb version
# Expected: Android Debug Bridge version X.X.X
```

### Test 3: Check Emulator

```powershell
emulator -list-avds
# Expected: List of your emulators
```

### Test 4: Check Connected Devices

```powershell
adb devices
# Expected: emulator-5554 device (if emulator is running)
```

---

## ✅ Success Checklist

- [ ] ANDROID_HOME variable is set
- [ ] PowerShell restarted after setting variables
- [ ] `adb version` command works
- [ ] Android SDK Platform 33 installed
- [ ] Android Emulator created and can boot
- [ ] `adb devices` shows emulator when running

---

## 🚀 Running the Mobile App

Once everything is set up:

### Terminal 1: Start FastAPI Backend
```powershell
cd backend/api
py main.py
# API at http://localhost:8000
```

### Terminal 2: Start React Native App
```powershell
cd mobile

# Option A: Run directly
npx react-native run-android

# Option B: Start Metro first
npx react-native start
# Then in another terminal:
npx react-native run-android
```

### Expected Output:
- Metro bundler starts
- Gradle builds Android app (first time: 5-10 minutes)
- App installs on emulator
- App opens automatically
- You see the Berlin Business Finder map!

---

## 🐛 Common Errors & Solutions

### Error: "ANDROID_HOME is not set"
**Solution:** Follow Step 2 above, restart PowerShell

### Error: "SDK location not found"
**Solution:** Open Android Studio, install Android SDK 33

### Error: "Unable to load script"
**Solution:**
```bash
npx react-native start --reset-cache
```

### Error: "Could not connect to development server"
**Solution:**
```bash
adb reverse tcp:8081 tcp:8081
adb reverse tcp:8000 tcp:8000
```

### Error: "Gradle build failed"
**Solution:**
```bash
cd android
gradlew clean
cd ..
npx react-native run-android
```

### Error: "No emulator found"
**Solution:**
- Open Android Studio
- Open AVD Manager
- Click ▶ Play on an emulator
- Wait for it to fully boot
- Try again

---

## 📊 Performance Tips

### For Faster Builds:
1. Use an SSD for Android SDK
2. Allocate more RAM to Android Studio
3. Use physical device (faster than emulator)
4. Enable Gradle daemon in `android/gradle.properties`

### For Smoother Map Performance:
1. Limit markers to 100-200 at a time
2. Use marker clustering (can be added later)
3. Test on physical device (better GPU)

---

## 📱 Testing on Physical Device

### USB Connection:

1. **Enable Developer Options on phone:**
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Developer Options unlocked!

2. **Enable USB Debugging:**
   - Settings → Developer Options
   - Turn on "USB Debugging"

3. **Connect phone via USB**

4. **Verify connection:**
```bash
adb devices
# Should show your device
```

5. **Run app:**
```bash
npx react-native run-android
```

---

## 🌐 API Configuration

The app connects to `http://localhost:8000`

**For production deployment:**

Edit `mobile/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://your-production-api.com/api/v1';
```

---

## 📖 Next Steps

1. ✅ Set up ANDROID_HOME (follow guide above)
2. ✅ Restart PowerShell
3. ✅ Verify with `adb version`
4. ✅ Start Android emulator
5. ✅ Start FastAPI backend (`py backend/api/main.py`)
6. ✅ Run mobile app (`npx react-native run-android`)

---

## 💡 Pro Tips

- **Use physical device** for best performance
- **Keep emulator running** between builds (faster)
- **Use `--verbose` flag** for detailed error messages
- **Check React Native docs** for latest guidance

---

## 🆘 Still Having Issues?

1. Check Android Studio SDK Manager - ensure all required components installed
2. Verify ANDROID_HOME with `echo $env:ANDROID_HOME`
3. Try running from Android Studio directly first
4. Check React Native environment: `npx react-native doctor`

---

**Good luck with your mobile app!** 📱🎉

