import os
import sys
import pytest
from app import app, db
from app.models import User, Reviews
from flask_login import login_user

sys.path.append(os.getcwd()[:-5] + "app")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables
        yield client
        # Clean up after tests
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def login_user(client):
    user = User(username="testuser", email="testuser@example.com")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()
    with client:
        login_user(user)
    yield client

@pytest.fixture
def create_review(client, login_user):
    review = Reviews(job_title="Sample Job", job_description="Job description", department="Dept",
                     locations="Location", hourly_pay=20, benefits="Benefits", review="Good", rating=5,
                     recommendation="Yes", author_id=1)  # Assume author_id=1 is the test user
    db.session.add(review)
    db.session.commit()
    return review

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_route_2(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_register_post(client):
    response = client.post('/register', data={'username': 'asavla2', 'password': 'pass', 'email': 'asavla2@ncsu.edu'})
    assert response.status_code == 200

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_login_post(client):
    response = client.post('/login', data={'email': 'asavla2@ncsu.edu', 'password': 'pass'})
    assert response.status_code == 200

def test_logout_get(client):
    response = client.get('/logout')
    assert response.status_code == 302

def test_view_review_all(client):
    response = client.get('/review/all')
    assert response.status_code == 200

def test_add_review_route_get(client):
    response = client.get('/review/new')
    assert response.status_code == 302

def test_add_review_route_post(client):
    response = client.post('/review/new', data={
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
    assert response.status_code == 302

def test_view_review(client, create_review):
    response1 = client.get('/review/1')  # Use the correct review ID created in the fixture
    response2 = client.get('/review/5')
    assert response1.status_code == 200
    assert response2.status_code == 404

def test_update_review_get(client, login_user, create_review):
    response = client.get('/review/1/update')  # Assuming the ID of the created review is 1
    assert response.status_code == 200

def test_update_review_post(client, login_user, create_review):
    response = client.post('/review/1/update', data={  # Use the correct review ID
        "job_title": "Updated Job Title",
        "job_description": "Updated Job Description",
        "department": "Updated Dept",
        "locations": "Updated Location",
        "hourly_pay": "25",
        "benefits": "Updated Benefits",
        "review": "Updated Review",
        "rating": "4",
        "recommendation": "No",
    })
    assert response.status_code == 302  # Redirect expected after a successful update

def test_update_review_unauthorized(client, create_review):
    # Simulate an unauthorized user trying to update a review
    unauthorized_user = User(username="unauthorized", email="unauth@example.com")
    unauthorized_user.set_password("wrongpassword")
    db.session.add(unauthorized_user)
    db.session.commit()
    with client:
        login_user(unauthorized_user)
        response = client.post('/review/1/update', data={
            "job_title": "Another Update",
            "job_description": "Another Update Description",
            "department": "Another Dept",
            "locations": "Another Location",
            "hourly_pay": "30",
            "benefits": "Another Benefits",
            "review": "Another Review",
            "rating": "3",
            "recommendation": "Yes",
        })
    assert response.status_code == 403  # Forbidden since user is not the author

def test_dashboard_route(client):
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_account_route(client):
    response = client.get('/account')
    assert response.status_code == 302

def test_get_jobs(client):
    response = client.get('/api/jobs')
    assert response.status_code == 200
