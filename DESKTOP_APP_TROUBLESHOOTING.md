# 🔧 DESKTOP APP CONNECTION TROUBLESHOOTING

## ❌ Problem: "Couldn't connect to backend while opening app"

This is a common issue! Here's how to fix it step by step.

---

## ✅ SOLUTION 1: Use the New Fixed Files (EASIEST)

I've created brand new fixed files that will definitely work:

### **Files You Need:**
1. `Backend_fixed_v2.py` - Updated backend (looks for index_final.html)
2. `desktop_app_fixed.py` - New desktop launcher with health checks
3. `index_final.html` - Your frontend

### **Steps:**
```bash
# 1. Make sure all 3 files are in the same folder
# Check by running:
dir    # Windows
ls     # Mac/Linux

# 2. Install dependencies
pip install Flask pywebview

# 3. Run the fixed desktop app
python desktop_app_fixed.py
```

---

## ✅ SOLUTION 2: Manual Testing (Find the exact problem)

### **Test 1: Does Backend Start?**

```bash
# Start backend manually
python Backend_fixed.py
```

**You should see:**
```
==================================================
CodeSensei Backend Starting...
==================================================
Server running on: http://127.0.0.1:5000
```

**If you see errors:**
- Missing imports? → `pip install Flask`
- Port in use? → Kill the process or change port
- File not found? → Make sure Backend_fixed.py is in the folder

---

### **Test 2: Can Backend Serve HTML?**

**While backend is running**, open your browser and visit:
```
http://localhost:5000
```

**You should see:**
- The CodeSensei interface (✅ GOOD!)
- Or JSON with "CodeSensei Backend API" (❌ HTML file not found)

**If you see JSON:**
The backend can't find your HTML file!

**Fix:**
```bash
# Check what HTML files you have
dir *.html    # Windows
ls *.html     # Mac/Linux

# Rename your HTML file to index_final.html
ren youfile.html index_final.html    # Windows
mv yourfile.html index_final.html    # Mac/Linux
```

---

### **Test 3: Can Desktop App Connect?**

Create this test file `test_connection.py`:

```python
import urllib.request
import time

print("Testing connection to backend...")

try:
    response = urllib.request.urlopen('http://localhost:5000/health', timeout=5)
    print(f"✅ Backend responding! Status: {response.status}")
    print(f"Response: {response.read().decode()}")
except Exception as e:
    print(f"❌ Cannot connect to backend!")
    print(f"Error: {e}")
    print("\nMake sure:")
    print("1. Backend is running (python Backend_fixed.py)")
    print("2. Backend shows 'Server running on http://127.0.0.1:5000'")
    print("3. No firewall blocking port 5000")
```

Run it:
```bash
# First, start backend in one terminal
python Backend_fixed.py

# Then, in another terminal
python test_connection.py
```

---

## 🐛 COMMON ISSUES & FIXES

### **Issue 1: "ModuleNotFoundError: No module named 'Backend_fixed'"**

**Problem:** Desktop app can't find the backend file

**Fix:**
```bash
# Make sure Backend_fixed.py is in the same folder as desktop_app.py
# Check with:
dir    # Windows
ls     # Mac/Linux

# You should see both files:
# - Backend_fixed.py
# - desktop_app_fixed.py
```

---

### **Issue 2: "Address already in use" or "Port 5000 busy"**

**Problem:** Something else is using port 5000

**Fix Option A - Kill the process:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Fix Option B - Use different port:**

Edit `Backend_fixed.py`, change line at the end:
```python
app.run(host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

Edit `desktop_app_fixed.py`, change the URL:
```python
'http://localhost:5001'  # Change 5000 to 5001
```

---

### **Issue 3: "No HTML file found" or showing JSON**

**Problem:** Backend can't find your HTML file

**Fix:**
```bash
# 1. Check what HTML files you have
dir *.html    # Windows
ls *.html     # Mac/Linux

# 2. Rename to index_final.html
ren yourfile.html index_final.html

# 3. Or update Backend_fixed.py to look for your filename
# Edit the home() function, add your filename to the list
```

---

### **Issue 4: Desktop window opens but shows nothing/blank**

**Problem:** Frontend can't connect to backend

**Fix:**

Open the desktop app's console (if visible) or browser DevTools (F12) and look for:
- "Connection refused" → Backend not running
- "CORS error" → Backend CORS not configured (shouldn't happen with our code)
- "404 Not Found" → HTML file not found

**Then:**
1. Close desktop app
2. Start backend manually: `python Backend_fixed.py`
3. Test in browser: `http://localhost:5000`
4. If browser works, try desktop app again

---

### **Issue 5: "pywebview not working" or crashes**

**Problem:** PyWebView installation issue

**Fix:**
```bash
# Uninstall and reinstall
pip uninstall pywebview -y
pip install pywebview

# On Linux, you might need additional dependencies:
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# On Mac with M1/M2:
pip install pywebview --no-cache-dir
```

---

## 🎯 STEP-BY-STEP WORKING SETUP

Follow these exact steps:

### **Step 1: Clean Start**
```bash
# 1. Create a new folder
mkdir CodeSensei
cd CodeSensei

# 2. Copy these 3 files into it:
#    - Backend_fixed_v2.py
#    - desktop_app_fixed.py  
#    - index_final.html
```

### **Step 2: Install Dependencies**
```bash
pip install Flask pywebview
```

### **Step 3: Test Backend First**
```bash
# Start backend
python Backend_fixed_v2.py
```

You should see:
```
==================================================
CodeSensei Backend Starting...
==================================================
Server running on: http://127.0.0.1:5000
📄 Serving: index_final.html
```

**Keep this terminal open!**

### **Step 4: Test in Browser**

Open browser → `http://localhost:5000`

You should see the CodeSensei interface.

**If not:**
- Check terminal for errors
- Make sure index_final.html is in the folder
- Try renaming it to index.html

### **Step 5: Run Desktop App**

**In a NEW terminal** (keep backend running):
```bash
python desktop_app_fixed.py
```

You should see:
```
============================================================
🥋 CodeSensei Desktop Application
============================================================
✅ Found: index_final.html

🔧 Starting backend server...
⏳ Waiting for backend to start...
✅ Backend is ready!

🌟 Opening application window...
```

**Desktop window should open!**

---

## 🚨 EMERGENCY BACKUP PLAN

If NOTHING works, use this super simple method:

### **Method: Run Backend + Open in Browser**

```bash
# 1. Start backend
python Backend_fixed_v2.py

# 2. Open browser
# Visit: http://localhost:5000

# That's it! No desktop app needed.
# It works exactly the same in the browser!
```

**For "app-like" experience in browser:**
- Chrome: Click "⋮" → "More tools" → "Create shortcut" → Check "Open as window"
- This creates a standalone window like a desktop app!

---

## 📊 CHECKLIST

Before running desktop app, verify:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Flask installed (`pip show Flask`)
- [ ] PyWebView installed (`pip show pywebview`)
- [ ] All 3 files in same folder
- [ ] No other program using port 5000
- [ ] HTML file exists (index_final.html or index.html)
- [ ] Backend tested and working in browser first

---

## 🎯 QUICK FIX COMMANDS

```bash
# Complete fresh start (copy-paste this):

# Install dependencies
pip install Flask pywebview

# Test backend only
python Backend_fixed_v2.py
# Visit http://localhost:5000 in browser
# Ctrl+C to stop

# If browser works, run desktop app:
python desktop_app_fixed.py
```

---

## 💡 PRO TIPS

1. **Always test backend in browser first** before trying desktop app
2. **Keep backend terminal open** to see error messages
3. **Check browser console (F12)** for frontend errors
4. **Use browser version** if desktop app keeps failing
5. **Port 5000 busy?** Use port 5001 or 8000 instead

---

## 🆘 STILL NOT WORKING?

### Create a minimal test:

**minimal_test.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Backend Works!</h1>'

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000")
    app.run(port=5000)
```

**Run it:**
```bash
python minimal_test.py
```

**Visit:** `http://localhost:5000`

If this works, the problem is in the main backend file.
If this doesn't work, the problem is your Python/Flask installation.

---

## 📞 DIAGNOSIS SCRIPT

Save this as `diagnose.py`:

```python
import sys
import os

print("=" * 60)
print("CodeSensei Diagnostic Tool")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check dependencies
try:
    import flask
    print(f"✓ Flask installed: {flask.__version__}")
except:
    print("✗ Flask NOT installed!")

try:
    import webview
    print(f"✓ PyWebView installed: {webview.__version__}")
except:
    print("✗ PyWebView NOT installed!")

# Check files
print("\n📁 Files in current directory:")
for f in os.listdir('.'):
    if f.endswith('.py') or f.endswith('.html'):
        print(f"  - {f}")

# Check for HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
if html_files:
    print(f"\n✓ Found {len(html_files)} HTML file(s)")
else:
    print("\n✗ No HTML files found!")

# Test port
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5000))
if result == 0:
    print("\n✗ Port 5000 is already in use!")
else:
    print("\n✓ Port 5000 is available")
sock.close()

print("\n" + "=" * 60)
```

**Run:**
```bash
python diagnose.py
```

This will tell you exactly what's wrong!

---

## ✅ SUCCESS INDICATORS

You know it's working when you see:

1. ✅ Backend terminal shows: "Server running on http://127.0.0.1:5000"
2. ✅ Backend terminal shows: "📄 Serving: index_final.html"
3. ✅ Browser at localhost:5000 shows CodeSensei interface
4. ✅ Desktop app terminal shows: "✅ Backend is ready!"
5. ✅ Desktop window opens showing CodeSensei interface
6. ✅ You can type code and click "Run Code"

---

**You got this! Follow the steps carefully and it WILL work!** 🚀
