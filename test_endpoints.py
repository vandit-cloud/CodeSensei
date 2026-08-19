import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_format():
    print("Testing /format...")
    messy_code = "def foo(  x ):\n  return x+1"
    response = requests.post(f"{BASE_URL}/format", json={"code": messy_code})
    if response.status_code == 200:
        print("[OK] /format Success")
        print(f"Original: {messy_code!r}")
        print(f"Formatted: {response.json().get('code')!r}")
    else:
        print(f"[FAIL] /format Failed: {response.text}")

def test_community_post():
    print("\nTesting /community (POST)...")
    snippet = {
        "title": "Test Snippet",
        "author": "Tester",
        "description": "A test snippet",
        "code": "print('Hello Community')"
    }
    response = requests.post(f"{BASE_URL}/community", json=snippet)
    if response.status_code == 200:
        print("[OK] /community POST Success")
        print(response.json())
    else:
        print(f"[FAIL] /community POST Failed: {response.text}")

def test_community_get():
    print("\nTesting /community (GET)...")
    response = requests.get(f"{BASE_URL}/community")
    if response.status_code == 200:
        snippets = response.json()
        print(f"[OK] /community GET Success. Found {len(snippets)} snippets.")
        if snippets:
            print(f"Latest: {snippets[0]['title']}")
    else:
        print(f"[FAIL] /community GET Failed: {response.text}")

if __name__ == "__main__":
    try:
        test_format()
        test_community_post()
        test_community_get()
    except Exception as e:
        print(f"[FAIL] Test script failed: {e}")
