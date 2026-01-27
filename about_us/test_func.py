import pytest
import json
import requests


def test_succes():
    response = requests.get('http://localhost:8000/api/about-us/structure')
    res = response.json()
    assert 'category' in res[0]

# def test_filter():
#     response = requests.get('http://localhost:8000/api/about-us/structure/')
