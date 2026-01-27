import pytest
import json
import requests


def test_succes():
    response = requests.get('http://localhost:8000/api/about-us/structure/?lang=kg')
    res = response.json()
    assert 'category' in res[0]
    assert isinstance(res[0]['category'], str)
    assert res[0]['is_active'] == False



# def test_filter():
#     response = requests.get('http://localhost:8000/api/about-us/structure/')
