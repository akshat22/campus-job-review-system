"""
This module initializes the Flask application and its extensions.
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import Config
from app.services.job_fetcher import fetch_job_listings

# Global variable to cache job listings
cached_jobs = []


def refresh_job_data():
    """Refresh the cached job data by fetching new listings."""
    global cached_jobs
    cached_jobs = fetch_job_listings()
    print(cached_jobs)
    socketio.emit("update_jobs", cached_jobs)

# Scheduler to refresh job data every 2 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_job_data, "interval", minutes=2)
print(scheduler)
scheduler.start()

# Initialize Flask application and extensions
app = Flask(__name__)
socketio = SocketIO(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
migrate = Migrate(app, db, render_as_batch=True)


@app.before_first_request
def create_table():
    """Create database tables before the first request."""
    db.create_all()
