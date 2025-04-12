import logging
import os
from app import app, db
from models import Plant, Remedy, PlantCategory, RemedyCategory, Benefit, Ingredient, PreparationStep, PlantImage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_plants():
    """Import Ayurvedic plants data into database"""
    logger.info("Starting Ayurvedic plants data import...")
    
    # Define a category for Ayurvedic plants
    category_name = "Ayurvedic Medicinal Plants"
    category = PlantCategory.query.filter_by(name=category_name).first()
    if not category:
        category = PlantCategory(name=category_name)
        db.session.add(category)
        logger.info(f"Created new plant category: {category_name}")
    
    # List of plants with their details
    plants_data = [
        {
            "name": "Neem",
            "scientific_name": "Azadirachta indica",
            "description": "Neem is one of the most important medicinal plants in India. Its leaves, bark, and seeds have been used in Ayurvedic medicine for thousands of years.",
            "usage": "Leaves are chewed fresh or used in tea; neem oil is used for hair and skincare.",
            "image_url": "/static/images/neem.png",
            "benefits": ["Antibacterial", "Antifungal", "Anti-inflammatory", "Immune-boosting", "Treats skin disorders", "Improves oral health", "Controls blood sugar levels"]
        },
        {
            "name": "Aloe Vera",
            "scientific_name": "Aloe barbadensis miller",
            "description": "Aloe Vera is a succulent plant with thick, fleshy leaves filled with a clear gel. It has been used for its medicinal properties for thousands of years.",
            "usage": "Aloe gel is applied for burns and skin issues; aloe juice is consumed for digestion.",
            "image_url": "/static/images/aloe_vera.png",
            "benefits": ["Cooling", "Anti-inflammatory", "Antioxidant", "Wound-healing", "Soothes burns", "Promotes digestion", "Hydrates skin", "Supports immunity"]
        },
        {
            "name": "Turmeric",
            "scientific_name": "Curcuma longa",
            "description": "Turmeric is a rhizomatous herbaceous perennial plant of the ginger family. The bright yellow spice is widely used in cooking and has potent medicinal properties.",
            "usage": "Used in cooking, taken with milk, or applied as a paste for wound healing.",
            "image_url": "/static/images/turmeric.png",
            "benefits": ["Anti-inflammatory", "Antioxidant", "Antimicrobial", "Reduces inflammation", "Boosts immunity", "Supports liver health", "Aids digestion"]
        },
        {
            "name": "Ginger",
            "scientific_name": "Zingiber officinale",
            "description": "Ginger is a flowering plant whose rhizome, ginger root or ginger, is widely used as a spice and a folk medicine. It has a warm, spicy flavor and aroma.",
            "usage": "Consumed fresh, dried, or in tea for digestion and colds.",
            "image_url": "/static/images/ginger.png",
            "benefits": ["Anti-nausea", "Digestive stimulant", "Anti-inflammatory", "Aids digestion", "Relieves nausea", "Reduces muscle pain", "Supports cardiovascular health"]
        },
        {
            "name": "Amla",
            "scientific_name": "Phyllanthus emblica",
            "description": "Amla, also known as Indian Gooseberry, is a deciduous tree that has edible fruit with a high vitamin C content. It's considered one of the most important medicinal plants in Ayurveda.",
            "usage": "Eaten raw, in juice, or as dried powder.",
            "image_url": "/static/images/amla.png",
            "benefits": ["Rich in vitamin C", "Antioxidant", "Immune-boosting", "Improves digestion", "Enhances skin health", "Strengthens immunity", "Regulates blood sugar"]
        },
        {
            "name": "Brahmi",
            "scientific_name": "Bacopa monnieri",
            "description": "Brahmi is a creeping herb with small white flowers that grows in wetlands and muddy shores. It's one of the most powerful brain tonics in Ayurveda.",
            "usage": "Consumed as a tea, powder, or in Ayurvedic formulations.",
            "image_url": "/static/images/brahmi.png",
            "benefits": ["Brain tonic", "Anti-anxiety", "Memory-enhancing", "Improves cognitive function", "Reduces stress", "Supports nervous system health"]
        },
        {
            "name": "Giloy",
            "scientific_name": "Tinospora cordifolia",
            "description": "Giloy is a herbaceous vine of the family Menispermaceae. In Ayurveda, it is known as 'Amrita', which means 'the root of immortality'.",
            "usage": "Consumed as juice, powder, or in decoction.",
            "image_url": "/static/images/giloy.png",
            "benefits": ["Immunomodulatory", "Antipyretic", "Anti-inflammatory", "Boosts immunity", "Treats fever", "Supports liver health", "Detoxifies the body"]
        },
        {
            "name": "Lemongrass",
            "scientific_name": "Cymbopogon citratus",
            "description": "Lemongrass is a tall perennial grass with a fresh, lemony aroma and a citrus flavor. It's a staple in Thai and other Asian cuisines and has many medicinal uses.",
            "usage": "Used in tea, essential oil, or fresh leaves in cooking.",
            "image_url": "/static/images/lemongrass.png",
            "benefits": ["Antioxidant", "Antibacterial", "Digestive aid", "Reduces stress", "Aids digestion", "Boosts metabolism", "Relieves headaches"]
        },
        {
            "name": "Mulethi",
            "scientific_name": "Glycyrrhiza glabra",
            "description": "Mulethi, also known as Licorice Root, has been used in traditional medicine in many parts of the world. It has a sweet taste and is often used in confectionery.",
            "usage": "Consumed as tea, powder, or herbal syrup.",
            "image_url": "/static/images/mulethi.png",
            "benefits": ["Anti-inflammatory", "Respiratory tonic", "Digestive aid", "Soothes sore throat", "Improves digestion", "Boosts respiratory health"]
        }
    ]
    
    # Import each plant
    for plant_data in plants_data:
        try:
            # Check if plant already exists
            existing_plant = Plant.query.filter_by(name=plant_data['name']).first()
            if existing_plant:
                logger.info(f"Plant '{plant_data['name']}' already exists, skipping")
                continue
            
            # Create plant
            plant = Plant(
                name=plant_data['name'],
                scientific_name=plant_data['scientific_name'],
                description=plant_data['description'],
                usage=plant_data['usage'],
                category=category
            )
            
            # Add benefits
            for benefit_name in plant_data['benefits']:
                # Find or create benefit
                benefit = Benefit.query.filter_by(name=benefit_name).first()
                if not benefit:
                    benefit = Benefit(name=benefit_name)
                    db.session.add(benefit)
                    logger.debug(f"Created new benefit: {benefit_name}")
                plant.benefits.append(benefit)
            
            # Add image
            image_url = plant_data.get('image_url')
            if image_url:
                plant.images.append(PlantImage(url=image_url, is_primary=True, alt_text=f"{plant_data['name']} image"))
            
            # Save to database
            db.session.add(plant)
            db.session.commit()
            logger.info(f"Successfully imported plant: {plant.name}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error importing plant {plant_data.get('name')}: {str(e)}")
    
    logger.info("Ayurvedic plants data import completed")

def import_remedies():
    """Import Ayurvedic remedies data into database"""
    logger.info("Starting Ayurvedic remedies data import...")
    
    # Define a category for Ayurvedic remedies
    category_name = "Traditional Ayurvedic Remedies"
    category = RemedyCategory.query.filter_by(name=category_name).first()
    if not category:
        category = RemedyCategory(name=category_name)
        db.session.add(category)
        logger.info(f"Created new remedy category: {category_name}")
    
    # Sample remedies - Add more as needed
    remedies_data = [
        {
            "name": "Turmeric Milk (Golden Milk)",
            "short_description": "A traditional Ayurvedic drink for boosting immunity",
            "description": "Golden Milk is a traditional Ayurvedic drink made with turmeric and other healing spices. It's known for its anti-inflammatory and immune-boosting properties.",
            "difficulty": "Easy",
            "usage": "Drink warm, preferably before bedtime. Can be consumed daily.",
            "ingredients": [
                "1 cup milk (or plant-based milk)",
                "1 teaspoon turmeric powder",
                "1/2 teaspoon cinnamon powder",
                "1/4 teaspoon ginger powder",
                "A pinch of black pepper",
                "Honey to taste (optional)"
            ],
            "preparation_steps": [
                "Heat the milk in a small saucepan over medium heat until it starts to simmer.",
                "Add turmeric, cinnamon, ginger, and black pepper.",
                "Whisk continuously until the mixture is well combined.",
                "Simmer on low heat for about 5-10 minutes.",
                "Remove from heat and add honey if desired.",
                "Strain into a cup and enjoy."
            ],
            "benefits": ["Boosts immunity", "Reduces inflammation", "Improves digestion", "Promotes better sleep"]
        },
        {
            "name": "Neem Face Pack",
            "short_description": "Natural remedy for acne and skin problems",
            "description": "Neem face pack is a traditional Ayurvedic remedy for various skin issues. Neem's antibacterial and antifungal properties make it excellent for treating acne, eczema, and other skin conditions.",
            "difficulty": "Easy",
            "usage": "Apply to clean face, avoid eye area. Leave on for 15-20 minutes, then rinse. Use 1-2 times per week.",
            "ingredients": [
                "2 tablespoons neem powder",
                "1 tablespoon sandalwood powder",
                "1 teaspoon turmeric powder",
                "Rose water (as needed)"
            ],
            "preparation_steps": [
                "Mix neem powder, sandalwood powder, and turmeric powder in a small bowl.",
                "Add enough rose water to form a smooth paste.",
                "Ensure the mixture has a spreadable consistency, not too thick or thin.",
                "Apply evenly to clean face, avoiding the eye area.",
                "Let it dry for 15-20 minutes.",
                "Rinse off with cool water, gently massaging in circular motions."
            ],
            "benefits": ["Treats acne", "Reduces inflammation", "Removes excess oil", "Improves skin texture"]
        },
        {
            "name": "Ginger-Honey Tea",
            "short_description": "Effective remedy for colds and sore throats",
            "description": "Ginger-honey tea is a simple yet effective remedy for colds, sore throats, and congestion. Ginger's warming properties help clear congestion, while honey soothes irritated throat tissues.",
            "difficulty": "Easy",
            "usage": "Drink warm, 2-3 times a day during illness. Can also be consumed regularly for general health.",
            "ingredients": [
                "1-inch piece of fresh ginger, sliced or grated",
                "1 cup water",
                "1 tablespoon honey",
                "1/2 lemon, juiced (optional)",
                "A pinch of cinnamon (optional)"
            ],
            "preparation_steps": [
                "Bring water to a boil in a small saucepan.",
                "Add sliced or grated ginger and reduce heat to low.",
                "Simmer for 5-10 minutes (longer for stronger tea).",
                "Remove from heat and strain into a cup.",
                "Add honey and lemon juice if using.",
                "Stir well and drink while warm."
            ],
            "benefits": ["Relieves sore throat", "Reduces congestion", "Boosts immunity", "Aids digestion"]
        }
    ]
    
    # Import each remedy
    for remedy_data in remedies_data:
        try:
            # Check if remedy already exists
            existing_remedy = Remedy.query.filter_by(name=remedy_data['name']).first()
            if existing_remedy:
                logger.info(f"Remedy '{remedy_data['name']}' already exists, skipping")
                continue
            
            # Create remedy
            remedy = Remedy(
                name=remedy_data['name'],
                short_description=remedy_data['short_description'],
                description=remedy_data['description'],
                difficulty=remedy_data['difficulty'],
                usage=remedy_data['usage'],
                category=category
            )
            
            # Add ingredients
            for i, ingredient_name in enumerate(remedy_data['ingredients']):
                remedy.ingredients.append(Ingredient(name=ingredient_name, order=i))
            
            # Add preparation steps
            for i, step_text in enumerate(remedy_data['preparation_steps']):
                remedy.preparation_steps.append(PreparationStep(description=step_text, step_number=i+1))
            
            # Add benefits
            for benefit_name in remedy_data['benefits']:
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
            logger.info(f"Successfully imported remedy: {remedy.name}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error importing remedy {remedy_data.get('name')}: {str(e)}")
    
    logger.info("Ayurvedic remedies data import completed")

def run_import():
    """Run the complete data import process"""
    with app.app_context():
        # Make sure all tables exist
        db.create_all()
        
        # Run imports
        import_plants()
        import_remedies()
        
        logger.info("Database import completed successfully")

if __name__ == "__main__":
    run_import()