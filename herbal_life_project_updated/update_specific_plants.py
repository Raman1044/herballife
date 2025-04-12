"""
Script to update specific plant images in the database
"""
import logging
from app import app, db
from models import Plant, PlantImage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def update_specific_plant_images():
    """Update images for specific plants in the database"""
    with app.app_context():
        plants_to_update = {
            "Ashwagandha": "/static/images/plants/ashwagandha.png",
            "Tulsi": "/static/images/plants/tulsi.png"
        }
        
        for plant_name, image_url in plants_to_update.items():
            # Find the plant
            plant = Plant.query.filter_by(name=plant_name).first()
            
            if not plant:
                logger.warning(f"Plant not found: {plant_name}")
                continue
            
            # Check if the plant has a primary image
            primary_image = PlantImage.query.filter_by(plant_id=plant.id, is_primary=True).first()
            
            if primary_image:
                # Update existing primary image
                primary_image.url = image_url
                logger.info(f"Updated primary image for {plant_name}")
            else:
                # Create new primary image
                plant_image = PlantImage(
                    plant_id=plant.id,
                    url=image_url,
                    alt_text=f"{plant_name} image",
                    is_primary=True
                )
                db.session.add(plant_image)
                logger.info(f"Created new primary image for {plant_name}")
        
        # Commit the changes
        db.session.commit()
        logger.info("Successfully updated specific plant images")

if __name__ == "__main__":
    update_specific_plant_images()