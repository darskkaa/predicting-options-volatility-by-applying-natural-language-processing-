"""
Local API Test Script for VOLA Engine

This script tests the API endpoints locally to ensure they work before deployment.
Run this script to verify your API is working correctly.
"""

import requests
import json
import time

def test_local_api():
    """Test the API endpoints locally"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing VOLA Engine API locally...")
    print("=" * 60)
    
    # Test endpoints
    tests = [
        {
            "name": "Root Endpoint",
            "endpoint": "/",
            "expected_status": 200
        },
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
            print("   ❌ FAIL - Connection error (API not running)")
            print("   💡 Start the API with: cd api && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            results.append(False)
        except requests.exceptions.Timeout:
            print("   ❌ FAIL - Timeout error")
            results.append(False)
        except Exception as e:
            print(f"   ❌ FAIL - Error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 LOCAL TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All local tests passed! Your API is working correctly.")
        print("🚀 Ready for deployment to Vercel!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Fix the issues before deploying.")
        return False

def start_api_instructions():
    """Print instructions for starting the API"""
    print("\n" + "=" * 60)
    print("🚀 STARTING THE API LOCALLY")
    print("=" * 60)
    print("1. Open a new terminal")
    print("2. Navigate to the api directory:")
    print("   cd vola-engine/api")
    print("3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("4. Start the API server:")
    print("   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("5. Keep the server running and run this test script in another terminal")
    print("=" * 60)

if __name__ == "__main__":
    print("🚀 VOLA Engine Local API Test")
    print("=" * 60)
    
    try:
        success = test_local_api()
        
        if not success:
            start_api_instructions()
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        start_api_instructions() 