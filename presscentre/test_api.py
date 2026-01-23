import pytest
import requests

@pytest.fixture
def base_url():
    return "http://localhost:8000/api/presscentre/"

def test_get_publications(base_url):
    response = requests.get(f"{base_url}publications/?lang=en")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]['title'] == "text(en)"