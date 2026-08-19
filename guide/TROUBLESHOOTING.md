# 🔧 TROUBLESHOOTING GUIDE

## "Couldn't connect to backend" - FIXED!

### ✅ EASIEST SOLUTION

**Use `backend_simple.py` - it only needs Flask!**

```bash
# 1. Install ONLY Flask
pip install Flask

# 2. Run the simple backend
python backend_simple.py

# 3. Open index.html in your browser
```

That's it! 🎉

---

## Step-by-Step Instructions

### 1️⃣ Install Flask
```bash
pip install Flask
```

If that doesn't work, try:
```bash
pip3 install Flask
# or
python -m pip install Flask
# or  
python3 -m pip install Flask
```

### 2️⃣ Start the Backend
```bash
python backend_simple.py
```

You should see:
```
==================================================
🚀 CodeSensei Backend Starting...
==================================================
✅ Server running on: http://127.0.0.1:5000
```

**Keep this terminal open!**

### 3️⃣ Open the Frontend

**Option A: Just open the file**
- Double-click `index.html`
- Or drag it into your browser

**Option B: Use a local server (recommended)**
```bash
# In a NEW terminal (keep backend running)
python -m http.server 8000
```
Then visit: http://localhost:8000

---

## 🐛 Common Issues

### Issue: "Module Flask not found"
**Fix:**
```bash
pip install Flask
```

### Issue: "Port 5000 already in use"
**Fix:** Kill whatever's using port 5000:
```bash
# Mac/Linux:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
# Note the PID, then:
taskkill /PID <NUMBER> /F
```

### Issue: Backend starts but frontend can't connect
**Fix:** Check if backend is actually running:
```bash
# In a new terminal:
curl http://127.0.0.1:5000/health
```

Should return: `{"status":"healthy","version":"2.0"}`

---

## ✅ Quick Test

Run this to verify everything works:

```bash
# 1. Check Python version (needs 3.7+)
python --version

# 2. Check Flask is installed
python -c "import flask; print('Flask OK')"

# 3. Start backend
python backend_simple.py
```

If all three work, you're good to go!

---

## 🆘 Still Having Issues?

Try the complete reset:

```bash
# 1. Stop everything (Ctrl+C in all terminals)

# 2. Reinstall Flask
pip uninstall Flask -y
pip install Flask

# 3. Start backend
python backend_simple.py

# 4. Open http://127.0.0.1:5000/health in browser
# Should show: {"status":"healthy","version":"2.0"}

# 5. Now open index.html
```

---

## Files You Need

1. `backend_simple.py` - The server (only needs Flask)
2. `index.html` - The web interface
3. `requirements_simple.txt` - Just says "Flask==3.0.0"

**That's all!** No RestrictedPython, no flask-cors needed.

---

## Success Checklist

- [ ] Python 3.7+ installed
- [ ] Flask installed (`pip list | grep Flask`)
- [ ] Backend running (shows startup message)
- [ ] Can access http://127.0.0.1:5000/health
- [ ] Browser console (F12) shows no errors
- [ ] "Run Code" button works
- [ ] "Analyze Performance" button works

All green? You're ready for the hackathon! 🚀
