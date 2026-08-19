"""
CodeSensei Desktop App - FIXED VERSION
Guaranteed to work!
"""

import webview
import threading
import time
import sys
import os

def start_backend():
    """Start the Flask backend"""
    try:
        print("=" * 60)
        print("🚀 Starting CodeSensei Backend...")
        print("=" * 60)
        
        # Import and start Flask
        from Backend_fixed_v2 import app
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        import traceback
        traceback.print_exc()

def check_backend_ready():
    """Check if backend is responding"""
    import urllib.request
    max_attempts = 10
    
    for i in range(max_attempts):
        try:
            response = urllib.request.urlopen('http://localhost:5000/health', timeout=1)
            if response.status == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def main():
    """Main application entry point"""
    print("=" * 60)
    print("🥋 CodeSensei Desktop Application")
    print("=" * 60)
    
    # Check if HTML files exist
    html_files = ['index_final.html', 'index_enhanced.html', 'index.html']
    found = False
    for f in html_files:
        if os.path.exists(f):
            print(f"✅ Found: {f}")
            found = True
            break
    
    if not found:
        print("❌ ERROR: No HTML file found!")
        print("Please ensure one of these files is in the same folder:")
        for f in html_files:
            print(f"  - {f}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start Flask backend in background
    print("\n🔧 Starting backend server...")
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to be ready
    print("⏳ Waiting for backend to start...")
    if check_backend_ready():
        print("✅ Backend is ready!")
    else:
        print("⚠️  Backend may not be fully ready, but continuing...")
    
    # Give it a bit more time
    time.sleep(1)
    
    print("\n🌟 Opening application window...")
    print("=" * 60)
    
    # Create window
    try:
        window = webview.create_window(
            'CodeSensei - Python Learning IDE',
            'http://localhost:5000',
            width=1400,
            height=900,
            resizable=True,
            min_size=(800, 600)
        )
        
        # Start webview
        webview.start(debug=False)
        
    except Exception as e:
        print(f"\n❌ Error creating window: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
