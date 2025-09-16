#!/usr/bin/env python3
"""
Test script to verify the calculate-simplified endpoint with corrected field names
"""
import requests
import json

def test_calculate_simplified_endpoint():
    """Test the calculate-simplified budget endpoint with correct field names"""
    
    # Endpoint URL
    url = "http://localhost:8002/api/v1/budgets/calculate-simplified"
    
    # JWT token (from previous session)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc1NTYyODcyNX0.M2Z9pgiVV5TVfv6chKF95cKECX6sio2Qkk_dlbiPj08"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Test data with CORRECTED field names (no quantity field)
    test_data = {
        "client_name": "Test Client",
        "items": [{
            "description": "Test Item",
            "weight": 10.0,  # Optional weight field
            "purchase_value_with_icms": 100.0,  # Correct field name
            "purchase_icms_percentage": 18.0,   # Correct field name (percentage format)
            "purchase_other_expenses": 0.0,     # Optional field
            "sale_value_with_icms": 150.0,      # Correct field name
            "sale_icms_percentage": 17.0        # Correct field name (percentage format)
        }],
        "notes": "Test budget calculation"
    }
    
    print("Testing calculate-simplified endpoint with CORRECTED field names...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        # Make the request
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS: Endpoint returned 200 OK")
            result = response.json()
            print("Response data:")
            print(json.dumps(result, indent=2, default=str))
            
            # Check if response has expected structure
            expected_fields = ['total_purchase_value', 'total_sale_value', 'total_commission', 'profitability_percentage', 'markup_percentage']
            missing_fields = [field for field in expected_fields if field not in result]
            
            if missing_fields:
                print(f"⚠️  WARNING: Missing expected fields: {missing_fields}")
            else:
                print("✅ Response has expected structure")
                
        else:
            print(f"❌ ERROR: Endpoint returned {response.status_code}")
            print("Response text:")
            print(response.text)
            
            if response.status_code == 422:
                print("❌ VALIDATION ERROR: Check field names and required fields")
                try:
                    error_data = response.json()
                    print("Error details:")
                    print(json.dumps(error_data, indent=2))
                except:
                    pass
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Could not connect to the server")
        print("Make sure Docker services are running with: docker compose up -d")
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR: Request timed out")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    test_calculate_simplified_endpoint()
