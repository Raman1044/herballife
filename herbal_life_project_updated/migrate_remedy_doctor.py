"""
Script to migrate existing remedies to have the doctor_id field
"""
import logging
from sqlalchemy import text
from app import app, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Run database migration to add doctor_id column to remedies table"""
    try:
        with app.app_context():
            # Check if doctor_id column exists in remedies table
            result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='remedy' AND column_name='doctor_id'"))
            if result.fetchone() is None:
                logger.info("Adding doctor_id column to remedy table")
                db.session.execute(text("ALTER TABLE remedy ADD COLUMN doctor_id INTEGER REFERENCES users(id)"))
                db.session.commit()
                logger.info("Successfully added doctor_id column to remedy table")
            else:
                logger.info("doctor_id column already exists in remedy table")
    except Exception as e:
        logger.error(f"Error in migration: {str(e)}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    run_migration()