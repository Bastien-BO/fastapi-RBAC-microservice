from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_api_create_user():
    ...


def test_api_delete_user():
    ...


def test_api_delete_users():
    ...


def test_api_put_user():
    ...


def test_api_get_user():
    ...


def test_api_get_users():
    ...


def test_api_me_user():
    ...
