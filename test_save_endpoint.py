#!/usr/bin/env python3
"""
Test script to verify the save-factor-groups endpoint works correctly
"""

import requests
import json

# Test data mimicking what the frontend would send
test_data = {
    "task_id": "test_task_123",
    "client": "PPG",
    "groups": [
        [
            {
                "id": 0,
                "original_statement": "I feel confident in my abilities",
                "aliasses": "Confidence Statement",
                "factor_groups": 1,
                "displayText": "Confidence Statement"
            },
            {
                "id": 1,
                "original_statement": "I believe in myself",
                "aliasses": "Self-Belief",
                "factor_groups": 1,
                "displayText": "Self-Belief"
            }
        ],
        [
            {
                "id": 2,
                "original_statement": "I work well with others",
                "aliasses": "Teamwork",
                "factor_groups": 2,
                "displayText": "Teamwork"
            }
        ],
        [
            {
                "id": 3,
                "original_statement": "I am creative",
                "aliasses": "Creativity",
                "factor_groups": 3,
                "displayText": "Creativity"
            }
        ],
        []  # Empty fourth group
    ]
}

def test_save_endpoint():
    """Test the save-factor-groups endpoint"""
    url = "http://127.0.0.1:8000/api/save-factor-groups"
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Save endpoint test PASSED!")
            print("Response:", json.dumps(result, indent=2))
            return True
        else:
            print(f"❌ Save endpoint test FAILED!")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("Testing save-factor-groups endpoint...")
    test_save_endpoint()
