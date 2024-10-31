import os
import sys

sys.path.append(os.getcwd()[:-5] + "app")
from app import app

# Basic route tests
def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_home_route():
    response = app.test_client().get('/home')
    assert response.status_code == 200

# Registration route tests
def test_register_route_get():
    response = app.test_client().get('/register')
    assert response.status_code == 200

def test_register_route_post():
    response = app.test_client().post('/register', data={
        'username': 'asavla2',
        'password': 'pass',
        'email': 'asavla2@ncsu.edu'
    })
    assert response.status_code == 200

# Login route tests
def test_login_route_get():
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_login_route_post():
    response = app.test_client().post('/login', data={
        'email': 'asavla2@ncsu.edu',
        'password': 'pass'
    })
    assert response.status_code == 200

# Logout route test
def test_logout_route():
    response = app.test_client().get('/logout')
    assert response.status_code == 302

# Review viewing and management route tests
def test_view_all_reviews():
    response = app.test_client().get('/review/all')
    assert response.status_code == 200

def test_create_review_get():
    response = app.test_client().get('/review/new')
    assert response.status_code == 302  # Redirects if not logged in

def test_create_review_post():
    response = app.test_client().post('/review/new', data={
        "job_title": "1",
        "job_description": "2",
        "department": "3",
        "locations": "4",
        "hourly_pay": "5",
        "benefits": "6",
        "review": "7",
        "rating": "2",
        "recommendation": "2",
    })
    assert response.status_code == 302  # Redirects if not logged in

def test_view_single_review():
    response = app.test_client().get('/review/5')
    assert response.status_code == 200  # Assumes review with ID 5 exists

    response = app.test_client().get('/review/1')
    assert response.status_code == 404  # Assumes review with ID 1 does not exist

def test_update_review_post():
    response = app.test_client().post('/review/5', data={
        "job_title": "1",
        "job_description": "2",
        "department": "3",
        "locations": "4",
        "hourly_pay": "5",
        "benefits": "6",
        "review": "7",
        "rating": "2",
        "recommendation": "2",
    })
    assert response.status_code == 405  # Method not allowed since update uses '/review/<id>/update'

# Page content filter test
def test_page_content_post():
    response = app.test_client().post('/pageContentPost', data={
        "search_title": "Developer",
        "search_location": "Raleigh",
        "min_rating": 3,
        "max_rating": 5
    })
    assert response.status_code == 200

# Vacancy and account routes
def test_dashboard_route():
    response = app.test_client().get('/dashboard')
    assert response.status_code == 200

def test_account_route():
    response = app.test_client().get('/account')
    assert response.status_code == 302  # Redirects if not logged in
