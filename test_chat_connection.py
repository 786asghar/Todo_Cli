# Test script to simulate how the frontend would call the backend
import requests
import json

# Test the chat API endpoint
def test_chat_api():
    url = "http://localhost:8000/api/chat/"

    # Test message
    payload = {
        "message": "Hello, this is a test message from the frontend!"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Sending test message to chat API...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            print("[SUCCESS] Chat API is working correctly!")
            return True
        else:
            print("[ERROR] Chat API returned an error")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to the backend server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing chat API connection...")
    test_chat_api()