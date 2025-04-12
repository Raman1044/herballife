import json
import logging
import os
from app import app, db
from models import Plant, Remedy, PlantCategory, RemedyCategory, Benefit, Ingredient, PreparationStep, PlantImage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading {filename}: {str(e)}")
        return None

def migrate_plants_data():
    """Migrate plants data from JSON to database"""
    logger.info("Starting plants data migration...")
    
    # Load plants data from JSON
    plants_data = load_json_file('static/js/data.json')
    if not plants_data or 'plants' not in plants_data:
        logger.error("No plants data found or invalid format")
        return
    
    plants_list = plants_data['plants']
    
    # Migrate each plant
    for plant_json in plants_list:
        try:
            # Check if plant already exists
            existing_plant = Plant.query.filter_by(name=plant_json['name']).first()
            if existing_plant:
                logger.info(f"Plant '{plant_json['name']}' already exists, skipping")
                continue
            
            # Find or create category
            category_name = plant_json.get('category', 'Uncategorized')
            category = PlantCategory.query.filter_by(name=category_name).first()
            if not category:
                category = PlantCategory(name=category_name)
                db.session.add(category)
                logger.info(f"Created new plant category: {category_name}")
            
            # Create plant
            plant = Plant(
                name=plant_json['name'],
                scientific_name=plant_json.get('scientific_name', ''),
                description=plant_json.get('description', ''),
                usage=plant_json.get('usage', ''),
                category=category
            )
            
            # Add benefits
            for benefit_name in plant_json.get('benefits', []):
                # Find or create benefit
                benefit = Benefit.query.filter_by(name=benefit_name).first()
                if not benefit:
                    benefit = Benefit(name=benefit_name)
                    db.session.add(benefit)
                    logger.debug(f"Created new benefit: {benefit_name}")
                plant.benefits.append(benefit)
            
            # Add image
            image_url = plant_json.get('image')
            if image_url:
                plant.images.append(PlantImage(url=image_url, is_primary=True))
            
            # Save to database
            db.session.add(plant)
            db.session.commit()
            logger.info(f"Successfully migrated plant: {plant.name}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error migrating plant {plant_json.get('name')}: {str(e)}")
    
    logger.info("Plants data migration completed")

def migrate_remedies_data():
    """Migrate remedies data from JSON to database"""
    logger.info("Starting remedies data migration...")
    
    # Load remedies data from JSON
    remedies_file = 'static/js/remedies.json'
    remedies_list = load_json_file(remedies_file)
    
    if not remedies_list:
        logger.error("No remedies data found or invalid format")
        return
    
    # Migrate each remedy
    for remedy_json in remedies_list:
        try:
            # Check if remedy already exists
            existing_remedy = Remedy.query.filter_by(name=remedy_json['name']).first()
            if existing_remedy:
                logger.info(f"Remedy '{remedy_json['name']}' already exists, skipping")
                continue
            
            # Find or create category
            category_name = remedy_json.get('category', 'Uncategorized')
            category = RemedyCategory.query.filter_by(name=category_name).first()
            if not category:
                category = RemedyCategory(name=category_name)
                db.session.add(category)
                logger.info(f"Created new remedy category: {category_name}")
            
            # Create remedy
            remedy = Remedy(
                name=remedy_json['name'],
                short_description=remedy_json.get('short_description', ''),
                description=remedy_json.get('description', ''),
                difficulty=remedy_json.get('difficulty', 'Medium'),
                usage=remedy_json.get('usage', ''),
                category=category
            )
            
            # Add ingredients
            for i, ingredient_name in enumerate(remedy_json.get('ingredients', [])):
                remedy.ingredients.append(Ingredient(name=ingredient_name, order=i))
            
            # Add preparation steps
            for i, step_text in enumerate(remedy_json.get('preparation_steps', [])):
                remedy.preparation_steps.append(PreparationStep(description=step_text, step_number=i+1))
            
            # Add benefits
            for benefit_name in remedy_json.get('benefits', []):
                # Find or create benefit
                benefit = Benefit.query.filter_by(name=benefit_name).first()
                if not benefit:
                    benefit = Benefit(name=benefit_name)
                    db.session.add(benefit)
                    logger.debug(f"Created new benefit: {benefit_name}")
                remedy.benefits.append(benefit)
            
            # Save to database
            db.session.add(remedy)
            db.session.commit()
            logger.info(f"Successfully migrated remedy: {remedy.name}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error migrating remedy {remedy_json.get('name')}: {str(e)}")
    
    logger.info("Remedies data migration completed")

def run_migration():
    """Run the complete data migration process"""
    with app.app_context():
        # Make sure all tables exist
        db.create_all()
        
        # Run migrations
        migrate_plants_data()
        migrate_remedies_data()
        
        logger.info("Database migration completed successfully")

if __name__ == "__main__":
    run_migration()
