"""
Script to update the plant images in the database with new image URLs
"""
import os
import logging
from app import app, db
from models import Plant, PlantImage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Define image URLs for each plant
PLANT_IMAGES = {
    "Neem": "/static/images/plants/neem.png",
    "Aloe Vera": "/static/images/plants/aloe_vera.png",
    "Turmeric": "/static/images/plants/turmeric.png",
    "Ginger": "/static/images/plants/ginger.png",
    "Amla": "/static/images/plants/amla.png",
    "Brahmi": "/static/images/plants/brahmi.png",
    "Giloy": "/static/images/plants/giloy.png",
    "Lemongrass": "/static/images/plants/lemongrass.png",
    "Mulethi": "/static/images/plants/mulethi.png"
}

def update_plant_images():
    """Update plant images with images from the provided files"""
    with app.app_context():
        # Create the static images directory if it doesn't exist
        os.makedirs("static/images/plants", exist_ok=True)
        
        # Copy the image files to the static directory
        source_files = {
            "Neem": "attached_assets/image_1743767674775.png",
            "Aloe Vera": "attached_assets/image_1743768075810.png",
            "Turmeric": "attached_assets/image_1743768087287.png",
            "Ginger": "attached_assets/image_1743768096366.png",
            "Amla": "attached_assets/image_1743768104509.png",
            "Brahmi": "attached_assets/image_1743768114376.png",
            "Giloy": "attached_assets/image_1743768126736.png",
            "Lemongrass": "attached_assets/image_1743768136210.png",
            "Mulethi": "attached_assets/image_1743768145175.png"
        }
        
        for plant_name, source_file in source_files.items():
            if os.path.exists(source_file):
                # Extract the filename from the source path
                target_file = f"static/images/plants/{plant_name.lower().replace(' ', '_')}.png"
                # Copy the file
                with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                    dst.write(src.read())
                logger.info(f"Copied image for {plant_name} to {target_file}")
            else:
                logger.warning(f"Source file for {plant_name} not found: {source_file}")
        
        # Update the database with image URLs
        for plant_name, image_url in PLANT_IMAGES.items():
            # Find the plant by name
            plant = Plant.query.filter(Plant.name.ilike(f"%{plant_name}%")).first()
            
            if plant:
                # Check if plant already has images
                if plant.images:
                    # Update existing primary image
                    primary_image = next((img for img in plant.images if img.is_primary), None)
                    if primary_image:
                        primary_image.url = image_url
                        logger.info(f"Updated primary image for {plant.name}")
                    else:
                        # Add as primary if no primary exists
                        new_image = PlantImage(
                            plant_id=plant.id,
                            url=image_url,
                            alt_text=f"{plant.name} image",
                            is_primary=True
                        )
                        db.session.add(new_image)
                        logger.info(f"Added new primary image for {plant.name}")
                else:
                    # Create new primary image
                    new_image = PlantImage(
                        plant_id=plant.id,
                        url=image_url,
                        alt_text=f"{plant.name} image",
                        is_primary=True
                    )
                    db.session.add(new_image)
                    logger.info(f"Added primary image for {plant.name}")
            else:
                logger.warning(f"Plant not found: {plant_name}")
        
        # Commit the changes
        db.session.commit()
        logger.info("Successfully updated plant images")

if __name__ == "__main__":
    update_plant_images()