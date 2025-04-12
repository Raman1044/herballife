"""
Script to update existing remedies with doctor associations
"""
import logging
from app import app, db
from models import Remedy, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_doctor_remedies():
    """Update existing remedies with doctor associations"""
    
    # Get doctors
    dr_chopra = User.query.filter_by(name=" Deepak Chopra").first()
    dr_lad = User.query.filter_by(name="Dr. Vasant Lad").first()
    dr_frawley = User.query.filter_by(name="Dr. David Frawley").first()
    
    if not all([dr_chopra, dr_lad, dr_frawley]):
        logger.error("Could not find all doctors in database")
        return
        
    # Remedy to doctor mappings
    remedy_mappings = [
        {"name": "Ginger Tea for Digestive Health", "doctor": dr_chopra},
        {"name": "Tulsi Tea for Cold & Flu", "doctor": dr_lad},
        {"name": "Triphala Powder for Digestion & Detox", "doctor": dr_lad},
        {"name": "Ashwagandha Milk for Stress & Energy", "doctor": dr_frawley},
        {"name": "Turmeric Golden Milk for Inflammation & Immunity", "doctor": dr_frawley}
    ]
    
    # Update remedies
    for mapping in remedy_mappings:
        remedy = Remedy.query.filter_by(name=mapping["name"]).first()
        if remedy:
            remedy.doctor = mapping["doctor"]
            logger.info(f"Updated remedy '{remedy.name}' with doctor: {mapping['doctor'].name}")
        else:
            logger.warning(f"Could not find remedy: {mapping['name']}")
    
    # Commit changes
    db.session.commit()
    logger.info("Completed updating doctor associations for remedies")

if __name__ == "__main__":
    with app.app_context():
        update_doctor_remedies()