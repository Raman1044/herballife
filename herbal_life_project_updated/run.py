"""
Herbal Life - Startup Script
This script first checks if the database exists and initializes it if needed,
then starts the Flask application.
"""

import os
import sys
import logging
from app import app  # Import the application instance

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check if the database file exists"""
    db_path = "herbal_life.db"
    return os.path.exists(db_path)

def initialize_database():
    """Initialize the database with sample data"""
    logger.info("Initializing database...")
    try:
        # Import and run the initialization with the app context
        with app.app_context():
            from initialize_database import run_initialization
            run_initialization()
        logger.info("Database initialization complete.")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def start_application():
    """Start the Flask application"""
    logger.info("Starting Herbal Life application...")
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    # Check if database exists, initialize if it doesn't
    if not check_database():
        success = initialize_database()
        if not success:
            logger.error("Database initialization failed. Exiting.")
            sys.exit(1)
    
    # Start the application
    start_application()