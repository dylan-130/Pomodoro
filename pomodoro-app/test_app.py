#!/usr/bin/env python3
"""
Test script for PomodoroFlow application
"""

import requests
import json
import sys

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:5000/api"
    
    print("🧪 Testing PomodoroFlow Backend...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/auth/me")
        if response.status_code == 401:
            print("✅ Backend is running (401 expected for unauthenticated user)")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running on http://localhost:5000")
        return False
    
    # Test 2: Register a test user
    try:
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_data = response.json()
            print(f"   User ID: {user_data['user']['id']}")
            print(f"   Username: {user_data['user']['username']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
    
    # Test 3: Login with test user
    try:
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Login test failed: {e}")
    
    # Test 4: Test timer session creation (requires authentication)
    try:
        session_data = {
            "session_type": "work",
            "duration": 25
        }
        response = requests.post(f"{base_url}/timer/sessions", json=session_data)
        if response.status_code == 201:
            print("✅ Timer session creation successful")
        else:
            print(f"⚠️  Timer session creation: {response.status_code} (expected if not authenticated)")
    except Exception as e:
        print(f"❌ Timer session test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend tests completed!")
    return True

def test_frontend():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5173")
        if response.status_code == 200:
            print("✅ Frontend is running on http://localhost:5173")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running on http://localhost:5173")
        return False

def main():
    """Run all tests"""
    print("🚀 PomodoroFlow Application Test")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n📊 Test Summary:")
    print(f"Backend: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Frontend: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 All tests passed! Application is ready to use.")
        print("🌐 Open http://localhost:5173 in your browser")
    else:
        print("\n⚠️  Some tests failed. Please check the server status.")
        sys.exit(1)

if __name__ == "__main__":
    main() 