import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    # create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "herbal_life_default_secret")

    # Configure the database
    # Use SQLite by default for local development, PostgreSQL for production
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        # Heroku provides DATABASE_URL in postgres:// format, but SQLAlchemy requires postgresql://
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    else:
        # Use SQLite for local development (no external database needed)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///herbal_life.db"
        app.logger.info("Using SQLite database for local development")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "login"  # Specify the login view route

    # Import routes after app is initialized to avoid circular imports
    with app.app_context():
        # Import models
        from models import Plant, Remedy, PlantCategory, RemedyCategory, PlantImage, User
        
        # User loader for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
            
        # Import and register routes
        from routes import register_routes
        register_routes(app)
        
        # Create all database tables
        db.create_all()
        
        app.logger.info("Database tables created successfully")
        
    return app

# Create the application instance
app = create_app()
