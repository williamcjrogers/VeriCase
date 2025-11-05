#!/usr/bin/env python3
"""
Test script for Railway deployment on port 8010
Run this to verify your deployment is working correctly
"""
import requests
import json
import sys
import time

def test_railway_deployment(base_url):
    """Test all key endpoints of the Railway deployment"""
    
    print(f"🚀 Testing Railway deployment at: {base_url}")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    def test_endpoint(name, url, method='GET', data=None, expected_status=200):
        nonlocal tests_passed, tests_total
        tests_total += 1
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == expected_status:
                print(f"✅ {name}: {response.status_code}")
                tests_passed += 1
                return True
            else:
                print(f"❌ {name}: {response.status_code} (expected {expected_status})")
                return False
                
        except Exception as e:
            print(f"❌ {name}: Failed - {str(e)}")
            return False
    
    # Test 1: Health endpoint
    test_endpoint("Health Check", f"{base_url}/health")
    
    # Test 2: Root endpoint
    test_endpoint("Root Endpoint", f"{base_url}/")
    
    # Test 3: UI Landing Page
    test_endpoint("Landing Page", f"{base_url}/ui/landing.html")
    
    # Test 4: UI Index Page
    test_endpoint("Index Page", f"{base_url}/ui/index.html")
    
    # Test 5: API Documentation
    test_endpoint("API Docs", f"{base_url}/docs")
    
    # Test 6: User Registration
    test_endpoint("User Registration", f"{base_url}/api/auth/register", 
                 method='POST', 
                 data={
                     "email": "test@example.com",
                     "password": "test123",
                     "full_name": "Test User"
                 },
                 expected_status=201)
    
    # Test 7: User Login
    test_endpoint("User Login", f"{base_url}/api/auth/login",
                 method='POST',
                 data={
                     "email": "test@example.com",
                     "password": "test123"
                 },
                 expected_status=200)
    
    # Test 8: Cases Endpoint (will likely fail without auth, but should return 401)
    test_endpoint("Cases Endpoint (Auth Required)", f"{base_url}/api/cases", expected_status=401)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! Your Railway deployment is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the logs and configuration.")
        return False

def main():
    # Get Railway URL from user or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        print("Enter your Railway URL (e.g., https://vericase-api-production.up.railway.app):")
        base_url = input().strip()
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    # Ensure https
    if not base_url.startswith('http'):
        base_url = 'https://' + base_url
    
    print(f"\n🔄 Waiting for deployment to be ready...")
    time.sleep(2)
    
    success = test_railway_deployment(base_url)
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Open your app in the browser")
        print("2. Create an admin account")
        print("3. Upload a PST file to test email processing")
        print("4. Explore all features")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check Railway build logs")
        print("2. Verify environment variables")
        print("3. Ensure database migrations ran")
        print("4. Check port configuration (should be 8010)")

if __name__ == "__main__":
    main()
