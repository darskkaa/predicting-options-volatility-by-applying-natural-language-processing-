"""
VOLA Engine Deployment Test Script

This script helps verify that your VOLA Engine API is working correctly after deployment.
Run this script to test your deployed API endpoints.
"""

import requests
import json
import sys
from datetime import datetime

def test_deployment(base_url):
    """Test the deployed API endpoints"""
    print(f"🔍 Testing VOLA Engine API at: {base_url}")
    print("=" * 60)
    
    # Test endpoints
    tests = [
        {
            "name": "Health Check",
            "endpoint": "/health",
            "expected_status": 200
        },
        {
            "name": "API Test",
            "endpoint": "/api/test", 
            "expected_status": 200
        },
        {
            "name": "Stock Analysis (AAPL)",
            "endpoint": "/api/analyze/AAPL",
            "expected_status": 200
        },
        {
            "name": "Sentiment Analysis (AAPL)",
            "endpoint": "/api/sentiment/AAPL",
            "expected_status": 200
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n📋 Testing: {test['name']}")
        print(f"   Endpoint: {test['endpoint']}")
        
        try:
            response = requests.get(f"{base_url}{test['endpoint']}", timeout=30)
            status = response.status_code
            print(f"   Status: {status}")
            
            if status == test['expected_status']:
                print("   ✅ PASS")
                if status == 200:
                    try:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)[:300]}...")
                    except:
                        print(f"   Response: {response.text[:200]}...")
                results.append(True)
            else:
                print("   ❌ FAIL - Unexpected status code")
                print(f"   Response: {response.text}")
                results.append(False)
                
        except requests.exceptions.ConnectionError:
            print("   ❌ FAIL - Connection error (API not reachable)")
            results.append(False)
        except requests.exceptions.Timeout:
            print("   ❌ FAIL - Timeout error")
            results.append(False)
        except Exception as e:
            print(f"   ❌ FAIL - Error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your VOLA Engine API is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
        return False

def main():
    """Main function to run deployment tests"""
    print("🚀 VOLA Engine Deployment Test")
    print("=" * 60)
    
    # Get base URL from user or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("Enter your API base URL (e.g., https://your-app.vercel.app): ").strip()
    
    if not base_url:
        print("❌ No base URL provided. Exiting.")
        return
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    print(f"\n🔗 Testing API at: {base_url}")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_deployment(base_url)
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Test your frontend application")
        print("2. Try searching for different stocks")
        print("3. Check that sentiment analysis works")
        print("4. Monitor your deployment logs")
    else:
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your Vercel deployment logs")
        print("2. Verify environment variables are set")
        print("3. Ensure all dependencies are installed")
        print("4. Check that the API routes are correctly configured")

if __name__ == "__main__":
    main() 