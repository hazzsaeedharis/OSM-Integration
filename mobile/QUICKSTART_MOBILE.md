# 🚀 Mobile App - Quick Start Guide

## ⚡ Fast Track to Running the App

### Prerequisites Checklist
- ✅ Node.js installed
- ✅ Android Studio installed
- ✅ React Native CLI: `npm install -g react-native-cli`
- ⚠️ **ANDROID_HOME** (see below)

---

## 🔥 Super Quick Setup (5 Minutes)

### 1. Set ANDROID_HOME (One Time Only)

**Find your SDK path** (usually):
```
C:\Users\h.haris\AppData\Local\Android\Sdk
```

**Set it in PowerShell** (AS ADMINISTRATOR):
```powershell
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Users\h.haris\AppData\Local\Android\Sdk", "User")

# Add to PATH
$path = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$path;$env:ANDROID_HOME\platform-tools", "User")
```

**Restart PowerShell!** ⚠️ (Important!)

**Verify:**
```powershell
adb version  # Should work now
```

---

### 2. Start Android Emulator

```powershell
# Open Android Studio → AVD Manager → Click Play on any emulator
# OR use command line:
emulator -list-avds
emulator -avd Pixel_5_API_33
```

---

### 3. Start Backend API

```powershell
# Terminal 1
cd "D:\Desktop\Test_Projects\1.5 Mill Cost reduction\OSM-Integration\backend\api"
py main.py
```

✅ API running at http://localhost:8000

---

### 4. Run Mobile App

```powershell
# Terminal 2 (NEW terminal)
cd "D:\Desktop\Test_Projects\1.5 Mill Cost reduction\OSM-Integration\mobile"
npx react-native run-android
```

**First build takes 5-10 minutes!** ⏳

---

## ✅ What You Should See

1. Metro Bundler starts (Terminal 2)
2. Gradle builds the app (1-10 minutes first time)
3. App installs on emulator
4. **Berlin Business Finder** app opens!
5. Map loads with Berlin view
6. You can search for businesses!

---

## 🎯 Quick Test (30 Seconds)

Once app opens:

1. ✅ See map with Berlin
2. ✅ Type "Restaurant" in search box
3. ✅ Tap search button (🔍)
4. ✅ See orange markers appear
5. ✅ Tap a marker → Popup shows
6. ✅ Switch to "Settings" tab → Toggle language

**If all 6 work → SUCCESS!** 🎉

---

## 🐛 Quick Troubleshooting

### Problem: "ANDROID_HOME not set"
```powershell
# Set it (see Step 1 above)
# MUST restart PowerShell after!
```

### Problem: "No devices found"
```powershell
# Start emulator first!
# Check with: adb devices
```

### Problem: "Cannot connect to Metro"
```powershell
# Run these commands:
adb reverse tcp:8081 tcp:8081
adb reverse tcp:8000 tcp:8000
```

### Problem: "Build failed"
```powershell
cd android
gradlew clean
cd ..
npx react-native run-android
```

---

## 📞 Need More Help?

- **Detailed setup**: See `ANDROID_SETUP.md`
- **Full README**: See `README.md`
- **React Native docs**: https://reactnative.dev/docs/environment-setup

---

## 🎉 Summary

```bash
# Set ANDROID_HOME → Restart PowerShell → Verify with adb
# Start emulator → Start API → Run mobile app
# DONE! 🚀
```

**Total time: ~10 minutes (first time), ~2 minutes (subsequent runs)**

