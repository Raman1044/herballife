"""
Script to add Holy Basil as an alternative name for Tulsi
"""
import logging
from app import app, db
from models import Plant, PlantCategory, PlantImage, Benefit, plant_benefits

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def get_or_create_category(name):
    """Get or create a plant category by name"""
    category = PlantCategory.query.filter_by(name=name).first()
    if not category:
        category = PlantCategory(name=name)
        db.session.add(category)
        logger.info(f"Created new category: {name}")
    return category

def get_or_create_benefit(name):
    """Get or create a benefit by name"""
    benefit = Benefit.query.filter_by(name=name).first()
    if not benefit:
        benefit = Benefit(name=name)
        db.session.add(benefit)
        logger.info(f"Created new benefit: {name}")
    return benefit

def add_holy_basil():
    """Add Holy Basil to the database"""
    with app.app_context():
        # First check if Tulsi exists
        tulsi = Plant.query.filter_by(name="Tulsi").first()
        
        # Data for Holy Basil
        plant_data = {
            "name": "Holy Basil",
            "scientific_name": "Ocimum sanctum",
            "category_name": "Medicinal Herbs",
            "description": "Holy Basil, also known as Tulsi, is a sacred plant in Hindu tradition. It's an aromatic perennial plant with many medicinal properties.",
            "usage": "Used in teas, tinctures, powders, and as a fresh herb. It's commonly consumed as a tea for respiratory issues and to boost immunity.",
            "benefits": [
                "Boosts immunity",
                "Reduces stress and anxiety",
                "Improves respiratory health",
                "Has antibacterial and antiviral properties",
                "Supports cardiovascular health"
            ],
            "image_url": "/static/images/plants/holy_basil.png"
        }
        
        # Check if Holy Basil already exists
        existing_plant = Plant.query.filter_by(name=plant_data["name"]).first()
        if existing_plant:
            logger.info(f"Plant already exists: {plant_data['name']}")
            return
        
        # Get or create category
        category = get_or_create_category(plant_data["category_name"])
        
        # Create the plant
        new_plant = Plant(
            name=plant_data["name"],
            scientific_name=plant_data["scientific_name"],
            description=plant_data["description"],
            usage=plant_data["usage"],
            category_id=category.id
        )
        db.session.add(new_plant)
        db.session.flush()  # Flush to get the plant ID
        
        # Add benefits
        for benefit_name in plant_data["benefits"]:
            benefit = get_or_create_benefit(benefit_name)
            new_plant.benefits.append(benefit)
        
        # Add image
        plant_image = PlantImage(
            plant_id=new_plant.id,
            url=plant_data["image_url"],
            alt_text=f"{plant_data['name']} image",
            is_primary=True
        )
        db.session.add(plant_image)
        
        logger.info(f"Added new plant: {plant_data['name']}")
        
        # Commit the changes
        db.session.commit()
        logger.info("Successfully added Holy Basil")

if __name__ == "__main__":
    add_holy_basil()