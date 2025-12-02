import pytest
import requests
from bs4 import BeautifulSoup

APP_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="module")
def session():
    with requests.Session() as s:
        yield s

def test_e2e_register_login_create_task(session):
    r = session.get(APP_URL + "/register")
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"] if soup.find("input", {"name": "csrf_token"}) else None

    data = {
        "username": "e2euser",
        "password": "e2epass",
        "confirm": "e2epass",
    }
    if csrf_token:
        data["csrf_token"] = csrf_token
    session.post(APP_URL + "/register", data=data)

    r = session.get(APP_URL + "/login")
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"] if soup.find("input", {"name": "csrf_token"}) else None

    data = {
        "username": "e2euser",
        "password": "e2epass",
    }
    if csrf_token:
        data["csrf_token"] = csrf_token
    session.post(APP_URL + "/login", data=data)

    r = session.get(APP_URL + "/tasks/new")
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"] if soup.find("input", {"name": "csrf_token"}) else None

    data = {
        "title": "E2E Task",
        "description": "Created by e2e test",
    }
    if csrf_token:
        data["csrf_token"] = csrf_token
    session.post(APP_URL + "/tasks/new", data=data)

    r = session.get(APP_URL + "/")
    assert "E2E Task" in r.text
