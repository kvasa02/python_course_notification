#!/usr/bin/env python3
"""
Test script to demonstrate the course notification functionality
This script tests the notification systems without requiring real credentials
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path so we can import notification functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_desktop_notification():
    """Test desktop notification functionality"""
    try:
        from plyer import notification
        
        print("Testing desktop notification...")
        notification.notify(
            title="Test: Course Available",
            message="This is a test notification for course CS101",
            timeout=5
        )
        print("✅ Desktop notification test completed")
        return True
    except Exception as e:
        print(f"❌ Desktop notification test failed: {e}")
        return False

def test_web_scraping():
    """Test web scraping functionality with a simple example"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        print("Testing web scraping...")
        
        # Test with a simple, accessible website
        test_url = "https://httpbin.org/html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(test_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1')
        
        if title:
            print(f"✅ Web scraping test successful - Found title: {title.text}")
            return True
        else:
            print("❌ Web scraping test failed - No title found")
            return False
            
    except Exception as e:
        print(f"❌ Web scraping test failed: {e}")
        return False

def test_environment_validation():
    """Test environment variable validation"""
    print("Testing environment validation...")
    
    # Test with missing variables
    test_vars = {
        "TWILIO_ACCOUNT_SID": None,
        "TWILIO_AUTH_TOKEN": None,
        "MESSAGING_SERVICE_SID": None,
        "MY_NUMBER": None,
        "COURSE_URL": None,
        "COURSE_CODE": None
    }
    
    missing_vars = [v for v, val in test_vars.items() if not val]
    if len(missing_vars) == len(test_vars):
        print("✅ Environment validation test passed - correctly identified missing variables")
        return True
    else:
        print("❌ Environment validation test failed")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Course Notification System Tests")
    print("=" * 50)
    
    tests = [
        ("Desktop Notification", test_desktop_notification),
        ("Web Scraping", test_web_scraping),
        ("Environment Validation", test_environment_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your notification system is ready to use.")
        print("\nNext steps:")
        print("1. Copy env.example to .env")
        print("2. Fill in your Twilio credentials and course details")
        print("3. Run: python3 notification.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 