"""
CodeSensei Diagnostic Tool
Run this to find out what's wrong!
"""

import sys
import os

def check_python():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
    return True

def check_dependencies():
    """Check required packages"""
    deps = []
    
    # Flask
    try:
        import flask
        # Use importlib to avoid deprecation warning
        try:
            import importlib.metadata
            version = importlib.metadata.version('flask')
        except:
            # Fallback to __version__ if importlib fails
            version = getattr(flask, '__version__', 'unknown')
        print(f"✓ Flask {version}")
        deps.append(True)
    except ImportError:
        print("✗ Flask NOT installed - Run: pip install Flask")
        deps.append(False)
    
    # PyWebView
    try:
        import webview
        # Try to get version, but don't fail if not available
        try:
            version = webview.__version__
        except AttributeError:
            # Newer PyWebView versions might not have __version__
            try:
                import importlib.metadata
                version = importlib.metadata.version('pywebview')
            except:
                version = "installed (version unknown)"
        print(f"✓ PyWebView {version}")
        deps.append(True)
    except ImportError:
        print("✗ PyWebView NOT installed - Run: pip install pywebview")
        deps.append(False)
    
    return all(deps)

def check_files():
    """Check required files"""
    print("\n📁 Files in current directory:")
    
    required_files = {
        'backend': ['Backend_fixed.py', 'Backend_fixed_v2.py', 'backend_simple.py'],
        'frontend': ['index_final.html', 'index_enhanced.html', 'index.html'],
        'launcher': ['desktop_app_fixed.py', 'desktop_app.py', 'run_desktop.py']
    }
    
    found = {
        'backend': None,
        'frontend': None,
        'launcher': None
    }
    
    all_files = os.listdir('.')
    
    for category, files in required_files.items():
        for file in files:
            if file in all_files:
                print(f"  ✓ {file}")
                found[category] = file
                break
    
    # Report missing
    missing = []
    if not found['backend']:
        print(f"  ✗ No backend file found! Need one of: {', '.join(required_files['backend'])}")
        missing.append('backend')
    
    if not found['frontend']:
        print(f"  ✗ No HTML file found! Need one of: {', '.join(required_files['frontend'])}")
        missing.append('frontend')
    
    if not found['launcher']:
        print(f"  ✗ No launcher file found! Need one of: {', '.join(required_files['launcher'])}")
        missing.append('launcher')
    
    return len(missing) == 0, found

def check_port():
    """Check if port 5000 is available"""
    import socket
    
    print("\n🔌 Port Status:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    
    if result == 0:
        print("  ✗ Port 5000 is ALREADY IN USE!")
        print("    Either:")
        print("    1. Kill the process using it")
        print("    2. Or the backend is already running (good!)")
        sock.close()
        return False
    else:
        print("  ✓ Port 5000 is available")
        sock.close()
        return True

def test_backend_connection():
    """Test if backend is responding"""
    import urllib.request
    
    print("\n🔗 Backend Connection Test:")
    try:
        response = urllib.request.urlopen('http://localhost:5000/health', timeout=2)
        if response.status == 200:
            print("  ✓ Backend is RUNNING and responding!")
            print("  → You can open http://localhost:5000 in browser")
            return True
    except:
        print("  ✗ Backend is NOT responding")
        print("  → Start it with: python Backend_fixed.py")
        return False

def main():
    print("=" * 70)
    print("🔍 CodeSensei Diagnostic Tool")
    print("=" * 70)
    
    print("\n📦 Checking Python & Dependencies:")
    python_ok = check_python()
    deps_ok = check_dependencies()
    
    files_ok, found_files = check_files()
    
    port_ok = check_port()
    backend_running = test_backend_connection()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    issues = []
    
    if not deps_ok:
        issues.append("Missing dependencies - Install with: pip install Flask pywebview")
    
    if not files_ok:
        issues.append("Missing required files - Make sure all files are in this folder")
    
    if not port_ok and not backend_running:
        issues.append("Port 5000 busy but backend not responding - Kill the process")
    
    if not backend_running and port_ok:
        issues.append("Backend not running - Start with: python Backend_fixed.py")
    
    if issues:
        print("\n⚠️  ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        print("\n🔧 RECOMMENDED ACTIONS:")
        if not deps_ok:
            print("  1. pip install Flask pywebview")
        if not backend_running:
            print(f"  2. python {found_files.get('backend', 'Backend_fixed.py')}")
        if found_files.get('frontend'):
            print("  3. Open http://localhost:5000 in browser to test")
        if found_files.get('launcher'):
            print(f"  4. python {found_files['launcher']}")
    else:
        print("\n✅ ALL CHECKS PASSED!")
        print("\n🚀 Ready to start:")
        if backend_running:
            print(f"  python {found_files.get('launcher', 'desktop_app_fixed.py')}")
        else:
            print(f"  1. python {found_files.get('backend', 'Backend_fixed.py')}")
            print(f"  2. python {found_files.get('launcher', 'desktop_app_fixed.py')}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
