import pytest
from delivery import app


@pytest.fixture(scope='module')
def client():
    app.testing = True
    client = app.test_client()
    return client


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_cart(client):
    response = client.get('/cart/')
    assert response.status_code == 200


def test_addtocart(client):
    response = client.get('/addtocart/')
    assert response.status_code == 200


def test_order_done(client):
    response = client.get('/order_done/')
    assert response.status_code == 200


def test_login(client):
    response = client.get('/auth/')
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout/')
    assert response.status_code == 302


def test_register(client):
    response = client.get('/register/')
    assert response.status_code == 200


def test_account(client):
    response = client.get('/account/')
    assert response.status_code == 302
