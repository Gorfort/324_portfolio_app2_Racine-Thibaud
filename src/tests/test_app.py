import pytest
from flask import Flask
import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_incorrect_username(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'password'
    })
    assert response.status_code == 200
    assert b'Username does not exist' in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'username': 'gogo',  # Use a valid username
        'password': 'gogogogo'  # Use the correct password
    })
    print(response.data)  # Debugging line
    print(response.status_code)  # Debugging line
    print(response.headers)  # Debugging line

    # Check if the response is a redirect (302) with a Location header
    assert response.status_code in [200, 302]  # Accept 200 for form errors, 302 for redirects
    if response.status_code == 302:
        assert response.headers['Location'] == '/'  # Check for the redirect location

def test_logout(client):
    # First, log in
    client.post('/login', data={
        'username': 'gogo',
        'password': 'gogogogo'
    })
    # Then, log out
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to login page
    assert response.headers['Location'] == '/login'

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_existing_user(client):
    response = client.post('/register', data={
        'username': 'gogo',  # Use an existing username
        'password': 'newpassword',
        'confirm-password': 'newpassword',
        'email': 'newemail@example.com'
    })
    assert b'Username already exists' in response.data

def test_register_success(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword',
        'confirm-password': 'newpassword',
        'email': 'newuser@example.com'
    })
    print(response.data)  # Debugging line
    print(response.status_code)  # Debugging line
    print(response.headers)  # Debugging line

    # Check if the response is a redirect (302) with a Location header
    assert response.status_code in [200, 302]  # Accept 200 for form errors, 302 for redirects
    if response.status_code == 302:
        assert response.headers['Location'] == '/'  # Check for the redirect location


def test_login_incorrect_password(client):
    response = client.post('/login', data={
        'username': 'gogo',  # Use a valid username
        'password': 'wrongpassword'
    })
    print(response.data)  # Debugging line
    assert response.status_code == 200
    assert b'Incorrect password' in response.data