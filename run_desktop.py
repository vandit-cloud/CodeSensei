"""
CodeSensei Desktop App - Ultimate Simple Version
Just works!
"""

import webview
import threading
import time

def start_backend():
    """Start the Flask backend"""
    from Backend_fixed_v2 import app
    app.run(port=5000, debug=False, use_reloader=False)

# Start backend in background
print("🚀 Starting CodeSensei...")
backend = threading.Thread(target=start_backend, daemon=True)
backend.start()

# Wait for it to start
time.sleep(2)

print("✅ Opening application...")

# Create window pointing to backend
webview.create_window(
    'CodeSensei - Python Learning IDE',
    'http://localhost:5000',
    width=1400,
    height=900
)

# Start the app
webview.start()
