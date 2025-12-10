import sys
import os
from fastapi.testclient import TestClient

# Add server directory to path
sys.path.append(os.path.join(os.getcwd(), "server"))

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "server is running"}
    print("Health check passed!")

def test_video_list():
    response = client.get("/videos/list")
    assert response.status_code == 200
    assert "videos" in response.json()
    print("Video list check passed!")

def test_conversation_empty():
    response = client.get("/questions/conversation/nonexistent")
    assert response.status_code == 200
    assert response.json() == {"video_id": "nonexistent", "conversation": []}
    print("Conversation check passed!")

if __name__ == "__main__":
    try:
        test_health()
        test_video_list()
        test_conversation_empty()
        print("\nAll basic checks passed! Backend structure is valid.")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        exit(1)
