import os
import sys
from flask import url_for

sys.path.append(os.getcwd()[:-5] + "app")
from app import app, db
from app.models import Reviews, User
from flask_login import login_user

# Set up user and review for testing
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

import time

def setup_module(module):
    # Clear user table to avoid duplicate email entries
    User.query.delete()
    db.session.commit()

    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
    test_user = User(username="testuser", email="testuser@ncsu.edu", password=hashed_password)
    db.session.add(test_user)
    db.session.commit()



    test_review = Reviews(
        job_title="Test Job",
        job_description="Testing description",
        department="IT",
        locations="Raleigh",
        hourly_pay="25",
        benefits="Health",
        review="Good experience",
        rating=4,
        recommendation=1,
        author_id=test_user.id,
    )
    db.session.add(test_review)
    db.session.commit()

def teardown_module(module):
    db.session.query(Reviews).delete()
    db.session.query(User).delete()
    db.session.commit()

# Test for updating a review by the author
def test_update_review_get_author_login():
    with app.test_client() as client:
        # Log in as the review author
        login_user(User.query.filter_by(username="testuser").first())
        review = Reviews.query.filter_by(job_title="Test Job").first()

        # Attempt to access update route
        response = client.get(f'/review/{review.id}/update')
        assert response.status_code == 200

        # Verify form fields are pre-populated with review data
        assert b'Test Job' in response.data
        assert b'Testing description' in response.data

# Test for unauthorized access to update a review
def test_update_review_unauthorized():
    with app.test_client() as client:
        # Create a new user and log in as them
        new_user = User(username="otheruser", email="otheruser@ncsu.edu")
        new_user.set_password("password")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        review = Reviews.query.filter_by(job_title="Test Job").first()

        # Attempt to access update route of a review by another user
        response = client.get(f'/review/{review.id}/update')
        assert response.status_code == 403  # Forbidden

# Test for successful review update
def test_update_review_post():
    with app.test_client() as client:
        # Log in as the review author
        login_user(User.query.filter_by(username="testuser").first())
        review = Reviews.query.filter_by(job_title="Test Job").first()

        # Submit updated review data
        response = client.post(f'/review/{review.id}/update', data={
            "job_title": "Updated Job",
            "job_description": "Updated description",
            "department": "Finance",
            "locations": "New York",
            "hourly_pay": "30",
            "benefits": "Dental",
            "review": "Great experience",
            "rating": 5,
            "recommendation": 1,
        }, follow_redirects=True)

        # Verify redirection and flash message
        assert response.status_code == 200
        assert b"Your review has been updated!" in response.data

        # Verify the review was updated in the database
        updated_review = Reviews.query.get(review.id)
        assert updated_review.job_title == "Updated Job"
        assert updated_review.department == "Finance"
        assert updated_review.rating == 5

# Test for API endpoint to fetch jobs
def test_get_jobs():
    with app.test_client() as client:
        response = client.get('/api/jobs')
        assert response.status_code == 200
        assert response.is_json
        assert isinstance(response.json, list)  # Assumes the response is a list of job listings
