"""
Script to add missing plants to the database
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

def add_missing_plants():
    """Add missing plants from the provided data"""
    with app.app_context():
        # Data for plants that were not found
        missing_plants = [
            {
                "name": "Aloe Vera",
                "scientific_name": "Aloe barbadensis miller",
                "category_name": "Medicinal Herbs",
                "description": "Aloe vera is a succulent plant species of the genus Aloe. It has thick, fleshy leaves that contain a gel-like substance used for various medicinal purposes.",
                "usage": "Aloe gel is applied for burns and skin issues; aloe juice is consumed for digestion. The gel is also commonly used in cosmetics and skincare products.",
                "benefits": [
                    "Soothes burns and skin irritations", 
                    "Promotes digestive health", 
                    "Hydrates skin", 
                    "Supports immune system"
                ],
                "image_url": "/static/images/plants/aloe_vera.png"
            },
            {
                "name": "Lemongrass",
                "scientific_name": "Cymbopogon citratus",
                "category_name": "Medicinal Herbs",
                "description": "Lemongrass is a tropical plant with long, aromatic leaves. It has a citrusy flavor and fragrance and is widely used in cooking and herbal medicine.",
                "usage": "Used in tea, essential oil, or as fresh leaves in cooking. The stalks are commonly used in Asian cuisine, particularly Thai and Vietnamese dishes.",
                "benefits": [
                    "Reduces stress and anxiety", 
                    "Aids digestion", 
                    "Boosts metabolism", 
                    "Relieves headaches", 
                    "Has antibacterial properties"
                ],
                "image_url": "/static/images/plants/lemongrass.png"
            },
            {
                "name": "Mulethi",
                "scientific_name": "Glycyrrhiza glabra",
                "category_name": "Medicinal Herbs",
                "description": "Mulethi, also known as Licorice root, is a perennial herb native to southern Europe and parts of Asia. It has been used in traditional medicine for thousands of years.",
                "usage": "Consumed as tea, powder, or herbal syrup. It's also used in Ayurvedic formulations for respiratory and digestive issues.",
                "benefits": [
                    "Soothes sore throat", 
                    "Improves digestion", 
                    "Boosts respiratory health", 
                    "Has anti-inflammatory properties",
                    "Supports adrenal gland function"
                ],
                "image_url": "/static/images/plants/mulethi.png"
            },
            {
                "name": "Tulsi",
                "scientific_name": "Ocimum sanctum",
                "category_name": "Medicinal Herbs",
                "description": "Tulsi, also known as Holy Basil, is a sacred plant in Hindu tradition. It's an aromatic perennial plant with many medicinal properties.",
                "usage": "Used in teas, tinctures, powders, and as a fresh herb. It's commonly consumed as a tea for respiratory issues and to boost immunity.",
                "benefits": [
                    "Boosts immunity",
                    "Reduces stress and anxiety",
                    "Improves respiratory health",
                    "Has antibacterial and antiviral properties",
                    "Supports cardiovascular health"
                ],
                "image_url": "/static/images/plants/tulsi.png"
            }
        ]
        
        for plant_data in missing_plants:
            # Check if plant already exists
            existing_plant = Plant.query.filter_by(name=plant_data["name"]).first()
            if existing_plant:
                logger.info(f"Plant already exists: {plant_data['name']}")
                continue
                
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
        logger.info("Successfully added missing plants")

if __name__ == "__main__":
    add_missing_plants()