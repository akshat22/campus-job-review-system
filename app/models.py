"""
This module contains the database models for the application,
including User, Reviews, and Vacancies.
"""

from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database given their user ID."""
    return User.query.get(int(user_id))


class Reviews(db.Model):
    """Model representing a review submitted by a user."""
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), index=True, nullable=False)
    locations = db.Column(db.String(120), index=True, nullable=False)
    job_title = db.Column(db.String(64), index=True, nullable=False)
    job_description = db.Column(db.String(120), index=True, nullable=False)
    hourly_pay = db.Column(db.String(10), nullable=False)
    benefits = db.Column(db.String(120), index=True, nullable=False)
    review = db.Column(db.String(120), index=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendation = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Vacancies(db.Model):
    """Model representing a job vacancy."""
    vacancy_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(500), index=True, nullable=False)
    job_description = db.Column(db.String(1000), index=True, nullable=False)
    job_location = db.Column(db.String(500), index=True, nullable=False)
    job_pay_rate = db.Column(db.String(120), index=True, nullable=False)
    max_hours_allowed = db.Column(db.Integer, nullable=False)

    def __init__(
        self, job_title, job_description, job_location, job_pay_rate, max_hours_allowed
    ):
        """Initialize a Vacancy instance."""
        self.job_title = job_title
        self.job_description = job_description
        self.job_location = job_location
        self.job_pay_rate = job_pay_rate
        self.max_hours_allowed = max_hours_allowed


class User(db.Model, UserMixin):
    """Model representing a user of the application."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    reviews = db.relationship("Reviews", backref="author", lazy=True)

    def __repr__(self):
        """Return a string representation of the User."""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
