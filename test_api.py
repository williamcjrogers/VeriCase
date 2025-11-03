#!/usr/bin/env python3
"""
VeriCase API End-to-End Test Script
Tests all critical API endpoints
"""
import requests
import json
import sys

API_BASE = "http://localhost:8010"

def test_auth():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication ===")
    
    # Test signup
    signup_data = {"email": f"testuser{hash('test')}@example.com", "password": "testpass123"}
    try:
        resp = requests.post(f"{API_BASE}/auth/signup", json=signup_data, timeout=5)
        if resp.status_code in [200, 409]:  # 409 if user exists
            print("✓ Signup endpoint working")
            if resp.status_code == 200:
                token = resp.json().get("token")
                return token
        else:
            print(f"✗ Signup failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"✗ Signup error: {e}")
        return None
    
    # Try login if signup returned 409
    try:
        resp = requests.post(f"{API_BASE}/auth/login", json=signup_data, timeout=5)
        if resp.status_code == 200:
            print("✓ Login endpoint working")
            return resp.json().get("token")
        else:
            print(f"✗ Login failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ Login error: {e}")
    
    return None

def test_documents(token):
    """Test document endpoints"""
    print("\n=== Testing Document Endpoints ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # List documents
    try:
        resp = requests.get(f"{API_BASE}/documents", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ List documents working - Found {data.get('total', 0)} documents")
        else:
            print(f"✗ List documents failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ List documents error: {e}")
    
    # List paths
    try:
        resp = requests.get(f"{API_BASE}/documents/paths", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ List paths working - Found {len(data.get('paths', []))} paths")
        else:
            print(f"✗ List paths failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ List paths error: {e}")

def test_folders(token):
    """Test folder endpoints"""
    print("\n=== Testing Folder Endpoints ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.get(f"{API_BASE}/folders", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ List folders working - Found {len(data.get('folders', []))} folders")
        else:
            print(f"✗ List folders failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ List folders error: {e}")

def test_search(token):
    """Test search endpoint"""
    print("\n=== Testing Search ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.get(f"{API_BASE}/search?q=test", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ Search working - Found {data.get('count', 0)} results")
        else:
            print(f"✗ Search failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"✗ Search error: {e}")

def check_services():
    """Check if all services are running"""
    print("\n=== Checking Services ===")
    
    services = {
        "API": f"{API_BASE}/",
        "OpenSearch": "http://localhost:9200/_cluster/health",
        "MinIO": "http://localhost:9002/minio/health/live"
    }
    
    for name, url in services.items():
        try:
            auth = ('admin', 'admin') if 'opensearch' in url.lower() else None
            resp = requests.get(url, auth=auth, timeout=3)
            if resp.status_code in [200, 307]:  # 307 for redirect
                print(f"✓ {name} is running")
            else:
                print(f"⚠ {name} returned {resp.status_code}")
        except Exception as e:
            print(f"✗ {name} is not accessible: {e}")

def main():
    print("=" * 60)
    print("VeriCase Docs - End-to-End Debug Test")
    print("=" * 60)
    
    # Check services
    check_services()
    
    # Test auth and get token
    token = test_auth()
    if not token:
        print("\n✗ Cannot proceed without authentication token")
        sys.exit(1)
    
    # Test other endpoints
    test_documents(token)
    test_folders(token)
    test_search(token)
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
