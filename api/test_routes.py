"""
Test script to verify API routes are working
"""
import requests
import json

def test_api_routes():
    """Test the API routes to ensure they're working"""
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        "/",
        "/health", 
        "/api/test",
        "/api/analyze/AAPL"
    ]
    
    print("Testing API endpoints...")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print("\nAPI route testing complete!")

if __name__ == "__main__":
    test_api_routes() 