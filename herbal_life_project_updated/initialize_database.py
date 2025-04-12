import os
import json
import logging
from app import db
from models import (
    User, PlantCategory, RemedyCategory, Plant, PlantImage, 
    Benefit, Remedy, Ingredient, PreparationStep, 
    plant_benefits, remedy_benefits
)
from werkzeug.security import generate_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_file(filename):
    """Load data from a JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filename}")
        return []

def create_categories():
    """Create initial plant and remedy categories"""
    plant_categories = [
        "Ayurvedic Medicinal Plants", 
        "Medicinal Herbs", 
        "Adaptogenic Plants",
        "Immunity Boosters", 
        "Digestive Herbs", 
        "Anti-inflammatory Plants", 
        "Skin Care Plants"
    ]
    
    remedy_categories = [
        "Traditional Ayurvedic Remedies",
        "Immunity Boosting Remedies",
        "Skin Care Remedies",
        "Cold & Flu Remedies",
        "Anti-inflammatory Preparations",
        "Digestive Health Remedies",
        "Stress Relief Remedies"
    ]
    
    # Create plant categories
    for category_name in plant_categories:
        if not PlantCategory.query.filter_by(name=category_name).first():
            category = PlantCategory(name=category_name)
            db.session.add(category)
    
    # Create remedy categories
    for category_name in remedy_categories:
        if not RemedyCategory.query.filter_by(name=category_name).first():
            category = RemedyCategory(name=category_name)
            db.session.add(category)
    
    db.session.commit()
    logger.info("Categories created successfully")

def create_doctors():
    """Create doctor accounts"""
    doctors = [
        {
            "name": "Dr. Deepak Chopra",
            "email": "deepak.chopra@example.com",
            "password": "password123",
            "is_doctor": True
        },
        {
            "name": "Dr. Vasant Lad",
            "email": "vasant.lad@example.com",
            "password": "password123",
            "is_doctor": True
        },
        {
            "name": "Dr. David Frawley",
            "email": "david.frawley@example.com",
            "password": "password123",
            "is_doctor": True
        }
    ]
    
    for doctor_data in doctors:
        email = doctor_data["email"]
        # Check if doctor already exists
        existing_doctor = User.query.filter_by(email=email).first()
        if not existing_doctor:
            # Create new doctor
            doctor = User(
                name=doctor_data["name"],
                email=email,
                is_doctor=doctor_data["is_doctor"]
            )
            doctor.password_hash = generate_password_hash(doctor_data["password"])
            db.session.add(doctor)
    
    # Create a regular user
    if not User.query.filter_by(email="user@example.com").first():
        user = User(
            name="Regular User",
            email="user@example.com",
            is_doctor=False
        )
        user.password_hash = generate_password_hash("password123")
        db.session.add(user)
    
    db.session.commit()
    logger.info("Doctors and test user created successfully")

def import_sample_plants():
    """Import sample plant data"""
    # Sample plants data
    plants_data = [
        {
            "name": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "description": "Ashwagandha is one of the most important herbs in Ayurveda. It has been used for over 3,000 years to help the body adapt to stress and promote overall wellness. The name Ashwagandha means 'smell of horse,' which refers to both the herb's scent and its traditional use to impart the vigor and strength of a stallion.",
            "usage": "Used as an adaptogen to help the body cope with daily stress and as a general tonic. Can be taken as a powder (1/4 to 1/2 teaspoon) mixed with warm milk or water, in capsule form (500-1000mg daily), or as a tea.",
            "category": "Adaptogenic Plants",
            "benefits": ["Reduces stress and anxiety", "Improves sleep quality", "Boosts immunity", "Enhances stamina and energy", "Supports healthy thyroid function", "May improve memory and cognitive function"],
            "images": [
                {
                    "url": "/static/images/image_1743708617893.png",
                    "alt_text": "Ashwagandha plant with berries",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Turmeric",
            "scientific_name": "Curcuma longa",
            "description": "Turmeric is a flowering plant of the ginger family. Its roots are widely used as a spice and for medicinal purposes. It contains curcumin, which has potent anti-inflammatory and antioxidant properties. For thousands of years, it has been used in Ayurvedic medicine for treating various conditions.",
            "usage": "Used as a spice in cooking (1/4 to 1 teaspoon daily), as a supplement in capsule form (400-600mg three times daily), or as a tea. Often mixed with black pepper to enhance absorption. Can also be applied topically as a paste for skin conditions.",
            "category": "Anti-inflammatory Plants",
            "benefits": ["Reduces inflammation", "Powerful antioxidant", "Improves brain function", "Lowers risk of heart disease", "Supports joint health", "May help prevent and treat certain cancers"],
            "images": [
                {
                    "url": "/static/images/image_1743708681884.png",
                    "alt_text": "Fresh turmeric root",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Holy Basil (Tulsi)",
            "scientific_name": "Ocimum sanctum",
            "description": "Tulsi is considered a sacred plant in Hinduism and is often planted around Hindu shrines. It has been used in Ayurveda for thousands of years for its healing properties. Known as 'The Incomparable One' and 'Mother Medicine of Nature,' it's revered for its remarkable healing properties.",
            "usage": "Consumed as tea (1-2 cups daily), in capsule form (300-600mg daily), or used in herbal preparations. Fresh leaves can be chewed or used in cooking. It can also be used in aromatherapy as an essential oil.",
            "category": "Immunity Boosters",
            "benefits": ["Reduces stress and anxiety", "Boosts immunity", "Enhances respiratory health", "Balances blood sugar", "Protects against infections", "Supports heart health"],
            "images": [
                {
                    "url": "/static/images/image_1743708721628.png",
                    "alt_text": "Holy Basil (Tulsi) plant with leaves",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Amla (Indian Gooseberry)",
            "scientific_name": "Phyllanthus emblica",
            "description": "Amla is one of the most important medicinal plants in Ayurveda. It contains one of the highest concentrations of vitamin C of any natural food. Amla is considered a rasayana (rejuvenative) that enhances longevity, boosts immunity, and promotes overall wellness.",
            "usage": "Can be consumed fresh, dried, or as juice, powder, or in supplement form. Often used in Ayurvedic formulations like Chyawanprash and Triphala. The recommended dose is 1-2 teaspoons of amla powder daily or 1 fresh fruit.",
            "category": "Immunity Boosters",
            "benefits": ["Rich in vitamin C and antioxidants", "Boosts immunity", "Improves digestion", "Enhances skin and hair health", "Supports liver function", "Balances blood sugar"],
            "images": [
                {
                    "url": "/static/images/image_1743708747322.png",
                    "alt_text": "Fresh Amla (Indian Gooseberry) fruits",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Neem",
            "scientific_name": "Azadirachta indica",
            "description": "Neem is known as 'Sarva Roga Nivarini' in Ayurveda, which means 'the curer of all ailments.' It has been used for thousands of years for its medicinal properties. Every part of the neem tree—leaves, flowers, seeds, fruit, roots, and bark—has distinct therapeutic value.",
            "usage": "Leaves can be used to make tea or taken in capsule form (300-500mg twice daily). Neem oil can be applied topically for skin conditions. Twigs are traditionally used as natural toothbrushes. Various preparations are used for different conditions.",
            "category": "Medicinal Herbs",
            "benefits": ["Powerful antibacterial properties", "Purifies blood", "Treats skin disorders", "Supports oral health", "Detoxifies the body", "Has insecticidal properties"],
            "images": [
                {
                    "url": "/static/images/image_1743708772480.png",
                    "alt_text": "Neem leaves and flowers",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Brahmi (Bacopa)",
            "scientific_name": "Bacopa monnieri",
            "description": "Brahmi is one of the most powerful brain tonics in Ayurvedic medicine. Named after 'Brahma,' the creator god in Hinduism, it's been used for centuries to enhance memory, learning, and concentration. It's considered a rasayana (rejuvenative) herb that promotes longevity and vitality.",
            "usage": "Can be taken as fresh juice (1-2 teaspoons daily), powder (1/4 to 1/2 teaspoon with warm water), or in capsule form (300-500mg daily). Also used in hair oils and as a medicated ghee. Best taken consistently for at least 3 months for cognitive benefits.",
            "category": "Adaptogenic Plants",
            "benefits": ["Enhances memory and cognitive function", "Reduces anxiety and stress", "Supports nervous system health", "Improves concentration and focus", "May help with ADHD symptoms", "Has antioxidant properties"],
            "images": [
                {
                    "url": "/static/images/image_1743708808895.png",
                    "alt_text": "Brahmi (Bacopa) plant with small flowers",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Giloy (Guduchi)",
            "scientific_name": "Tinospora cordifolia",
            "description": "Giloy is known as 'Amrita' in Ayurveda, which means 'the root of immortality.' It's one of the most versatile herbs in Ayurvedic medicine, classified as a rasayana (rejuvenative). Giloy is known for its immune-boosting, anti-inflammatory, and adaptogenic properties.",
            "usage": "Can be taken as a powder (1/2 teaspoon with warm water), juice (2 tablespoons daily), or in capsule form (500mg twice daily). Also used in various Ayurvedic formulations. Should be taken under professional guidance for specific health conditions.",
            "category": "Immunity Boosters",
            "benefits": ["Boosts immunity", "Treats fever and infections", "Detoxifies the body", "Reduces inflammation", "Balances blood sugar", "Improves digestive health"],
            "images": [
                {
                    "url": "/static/images/image_1743708853809.png",
                    "alt_text": "Giloy (Guduchi) vine and leaves",
                    "is_primary": True
                }
            ]
        },
        {
            "name": "Ginger",
            "scientific_name": "Zingiber officinale",
            "description": "Ginger is one of the oldest medicinal spices in Ayurvedic tradition. Known as 'Vishwabhesaj' or 'universal medicine,' it's highly regarded for its warming, digestive, and anti-inflammatory properties. Used in fresh, dried, or powdered form, ginger is both a culinary spice and a powerful therapeutic herb.",
            "usage": "Can be used fresh in cooking, steeped as tea (1-inch piece or 1 teaspoon powder per cup), taken in capsule form (250-500mg 2-3 times daily), or applied externally as oil or paste. Often combined with honey or lemon for colds and digestive issues.",
            "category": "Digestive Herbs",
            "benefits": ["Aids digestion", "Reduces nausea and vomiting", "Relieves joint pain", "Fights respiratory infections", "Improves circulation", "Has anti-inflammatory effects"],
            "images": [
                {
                    "url": "/static/images/image_1743708926498.png",
                    "alt_text": "Fresh ginger root",
                    "is_primary": True
                }
            ]
        }
    ]
    
    for plant_data in plants_data:
        # Check if plant already exists
        if Plant.query.filter_by(name=plant_data["name"]).first():
            continue
        
        # Get or create category
        category = PlantCategory.query.filter_by(name=plant_data["category"]).first()
        if not category:
            category = PlantCategory(name=plant_data["category"])
            db.session.add(category)
            db.session.flush()
        
        # Create plant
        plant = Plant(
            name=plant_data["name"],
            scientific_name=plant_data["scientific_name"],
            description=plant_data["description"],
            usage=plant_data["usage"],
            category_id=category.id
        )
        db.session.add(plant)
        db.session.flush()
        
        # Add benefits
        for benefit_name in plant_data["benefits"]:
            benefit = Benefit.query.filter_by(name=benefit_name).first()
            if not benefit:
                benefit = Benefit(name=benefit_name)
                db.session.add(benefit)
                db.session.flush()
            
            # Check if the benefit is already associated with the plant
            if not db.session.query(plant_benefits).filter_by(
                plant_id=plant.id, benefit_id=benefit.id
            ).first():
                # Add the association
                stmt = plant_benefits.insert().values(
                    plant_id=plant.id, benefit_id=benefit.id
                )
                db.session.execute(stmt)
        
        # Add images
        for image_data in plant_data["images"]:
            image = PlantImage(
                plant_id=plant.id,
                url=image_data["url"],
                alt_text=image_data["alt_text"],
                is_primary=image_data.get("is_primary", False)
            )
            db.session.add(image)
    
    db.session.commit()
    logger.info("Sample plants imported successfully")

def import_sample_remedies():
    """Import sample remedy data"""
    # Sample remedies data
    remedies_data = [
        # Dr. Deepak Chopra's remedies
        {
            "name": "Ginger Tea for Digestive Health",
            "short_description": "A soothing ginger tea to improve digestion and reduce inflammation",
            "description": "Ginger Tea is a simple yet effective Ayurvedic remedy for digestive issues. The active compounds in ginger help stimulate digestion, reduce inflammation, and soothe the digestive tract.",
            "difficulty": "Easy",
            "usage": "Drink warm, preferably before or after meals to aid digestion. Can be consumed 1-2 times daily.",
            "category": "Digestive Health Remedies",
            "doctor_email": "deepak.chopra@example.com",
            "benefits": ["Relieves gas and bloating", "Improves digestion", "Reduces inflammation", "Soothes nausea"],
            "ingredients": [
                {"name": "1-inch fresh ginger root (grated or sliced)", "order": 1},
                {"name": "2 cups water", "order": 2},
                {"name": "1 tsp honey (optional)", "order": 3},
                {"name": "1/2 tsp lemon juice (optional)", "order": 4}
            ],
            "preparation_steps": [
                {"description": "Boil 2 cups of water in a saucepan.", "step_number": 1},
                {"description": "Add the grated/sliced ginger and let it simmer for 5–10 minutes.", "step_number": 2},
                {"description": "Strain the tea into a cup.", "step_number": 3},
                {"description": "Add honey and lemon juice if desired.", "step_number": 4},
                {"description": "Drink warm, preferably before or after meals.", "step_number": 5}
            ]
        },
        {
            "name": "Golden Milk",
            "short_description": "A soothing turmeric drink with anti-inflammatory properties",
            "description": "Golden Milk is a traditional Ayurvedic drink that combines turmeric with milk and other spices. It has powerful anti-inflammatory and antioxidant properties.",
            "difficulty": "Easy",
            "usage": "Drink warm before bedtime to promote relaxation and reduce inflammation. Can be consumed daily.",
            "category": "Anti-inflammatory Preparations",
            "doctor_email": "deepak.chopra@example.com",
            "benefits": ["Reduces inflammation", "Improves sleep quality", "Supports immune system", "Aids digestion"],
            "ingredients": [
                {"name": "Milk or plant-based milk - 1 cup", "order": 1},
                {"name": "Ground turmeric - 1/2 teaspoon", "order": 2},
                {"name": "Ground cinnamon - 1/4 teaspoon", "order": 3},
                {"name": "Ground ginger - 1/4 teaspoon", "order": 4},
                {"name": "Black pepper - A pinch", "order": 5},
                {"name": "Honey or maple syrup (optional) - to taste", "order": 6}
            ],
            "preparation_steps": [
                {"description": "In a small saucepan, heat the milk over medium heat until it's warm but not boiling.", "step_number": 1},
                {"description": "Add turmeric, cinnamon, ginger, and black pepper to the milk.", "step_number": 2},
                {"description": "Whisk to combine and continue to heat for about 3-5 minutes.", "step_number": 3},
                {"description": "Remove from heat and add honey or maple syrup if desired.", "step_number": 4},
                {"description": "Strain if needed and serve warm.", "step_number": 5}
            ]
        },
        
        # Dr. Vasant Lad's remedies
        {
            "name": "Tulsi Tea for Cold & Flu",
            "short_description": "A healing herbal tea to boost immunity and relieve cold symptoms",
            "description": "Tulsi (Holy Basil) is considered a sacred herb in Ayurveda with powerful immunomodulatory properties. This simple tea preparation helps combat cold, flu, and respiratory infections.",
            "difficulty": "Easy",
            "usage": "Drink 2-3 cups daily when experiencing cold symptoms, or 1 cup daily for prevention.",
            "category": "Cold & Flu Remedies",
            "doctor_email": "vasant.lad@example.com",
            "benefits": ["Strengthens immunity", "Relieves cough and congestion", "Reduces fever", "Soothes sore throat"],
            "ingredients": [
                {"name": "5–6 fresh tulsi (holy basil) leaves", "order": 1},
                {"name": "1 cup water", "order": 2},
                {"name": "1/2 tsp honey (optional)", "order": 3},
                {"name": "1/4 tsp black pepper (optional)", "order": 4}
            ],
            "preparation_steps": [
                {"description": "Boil the tulsi leaves in 1 cup of water for 5 minutes.", "step_number": 1},
                {"description": "Strain and pour into a cup.", "step_number": 2},
                {"description": "Add honey and black pepper if desired.", "step_number": 3},
                {"description": "Drink warm to relieve cold, cough, and flu symptoms.", "step_number": 4}
            ]
        },
        {
            "name": "Triphala Powder for Digestion & Detox",
            "short_description": "A traditional digestive and detoxifying Ayurvedic formula",
            "description": "Triphala is a classic Ayurvedic formulation consisting of three fruits: Amalaki, Bibhitaki, and Haritaki. This balanced blend supports digestion, gentle detoxification, and overall health.",
            "difficulty": "Easy",
            "usage": "Take daily before bed for digestive health and gentle detoxification.",
            "category": "Digestive Health Remedies",
            "doctor_email": "vasant.lad@example.com",
            "benefits": ["Supports digestion", "Detoxifies the body", "Improves absorption of nutrients", "Promotes regular elimination"],
            "ingredients": [
                {"name": "1 tsp Triphala powder", "order": 1},
                {"name": "1 cup warm water", "order": 2},
                {"name": "Honey (optional) to taste", "order": 3}
            ],
            "preparation_steps": [
                {"description": "Mix 1 tsp of Triphala powder in warm water.", "step_number": 1},
                {"description": "Add honey if desired (Triphala is quite bitter).", "step_number": 2},
                {"description": "Stir well and drink before bed.", "step_number": 3}
            ]
        },
        
        # Dr. David Frawley's remedies
        {
            "name": "Ashwagandha Milk for Stress & Energy",
            "short_description": "A rejuvenating tonic for stress relief and energy balance",
            "description": "Ashwagandha is one of Ayurveda's most powerful adaptogenic herbs. This nighttime milk preparation helps balance the body's stress response, promotes restful sleep, and builds sustainable energy.",
            "difficulty": "Easy",
            "usage": "Drink daily before bedtime to reduce stress and build vitality.",
            "category": "Stress Relief Remedies",
            "doctor_email": "david.frawley@example.com",
            "benefits": ["Reduces stress and anxiety", "Boosts strength and stamina", "Improves sleep quality", "Balances hormones"],
            "ingredients": [
                {"name": "1 tsp Ashwagandha powder", "order": 1},
                {"name": "1 cup warm milk", "order": 2},
                {"name": "1/2 tsp honey (optional)", "order": 3},
                {"name": "1/4 tsp cinnamon (optional)", "order": 4}
            ],
            "preparation_steps": [
                {"description": "Warm a cup of milk.", "step_number": 1},
                {"description": "Add Ashwagandha powder and stir well.", "step_number": 2},
                {"description": "Add honey or cinnamon if desired.", "step_number": 3},
                {"description": "Drink before bedtime for relaxation and vitality.", "step_number": 4}
            ]
        },
        {
            "name": "Turmeric Golden Milk for Inflammation & Immunity",
            "short_description": "A healing golden milk preparation for inflammation and immune support",
            "description": "This classic Ayurvedic preparation combines the anti-inflammatory power of turmeric with black pepper for enhanced bioavailability. Golden milk is traditionally used to reduce inflammation, strengthen immunity, and promote overall wellness.",
            "difficulty": "Easy",
            "usage": "Drink daily before bed for anti-inflammatory benefits and immune support.",
            "category": "Immunity Boosting Remedies",
            "doctor_email": "david.frawley@example.com",
            "benefits": ["Reduces joint pain and inflammation", "Strengthens immunity", "Improves digestion", "Supports liver function"],
            "ingredients": [
                {"name": "1 cup milk (dairy or plant-based)", "order": 1},
                {"name": "1/2 tsp turmeric powder", "order": 2},
                {"name": "1/4 tsp black pepper", "order": 3},
                {"name": "1/2 tsp honey (optional)", "order": 4}
            ],
            "preparation_steps": [
                {"description": "Warm the milk in a saucepan.", "step_number": 1},
                {"description": "Add turmeric and black pepper. Stir well.", "step_number": 2},
                {"description": "Add honey for sweetness if desired.", "step_number": 3},
                {"description": "Drink before bed for better immunity and anti-inflammatory benefits.", "step_number": 4}
            ]
        }
    ]
    
    for remedy_data in remedies_data:
        # Check if remedy already exists
        if Remedy.query.filter_by(name=remedy_data["name"]).first():
            continue
        
        # Get or create category
        category = RemedyCategory.query.filter_by(name=remedy_data["category"]).first()
        if not category:
            category = RemedyCategory(name=remedy_data["category"])
            db.session.add(category)
            db.session.flush()
        
        # Get doctor
        doctor = User.query.filter_by(email=remedy_data["doctor_email"]).first()
        
        # Create remedy
        remedy = Remedy(
            name=remedy_data["name"],
            short_description=remedy_data["short_description"],
            description=remedy_data["description"],
            difficulty=remedy_data["difficulty"],
            usage=remedy_data["usage"],
            category_id=category.id,
            doctor_id=doctor.id if doctor else None
        )
        db.session.add(remedy)
        db.session.flush()
        
        # Add benefits
        for benefit_name in remedy_data["benefits"]:
            benefit = Benefit.query.filter_by(name=benefit_name).first()
            if not benefit:
                benefit = Benefit(name=benefit_name)
                db.session.add(benefit)
                db.session.flush()
            
            # Check if the benefit is already associated with the remedy
            if not db.session.query(remedy_benefits).filter_by(
                remedy_id=remedy.id, benefit_id=benefit.id
            ).first():
                # Add the association
                stmt = remedy_benefits.insert().values(
                    remedy_id=remedy.id, benefit_id=benefit.id
                )
                db.session.execute(stmt)
        
        # Add ingredients
        for ingredient_data in remedy_data["ingredients"]:
            ingredient = Ingredient(
                remedy_id=remedy.id,
                name=ingredient_data["name"],
                order=ingredient_data["order"]
            )
            db.session.add(ingredient)
        
        # Add preparation steps
        for step_data in remedy_data["preparation_steps"]:
            step = PreparationStep(
                remedy_id=remedy.id,
                description=step_data["description"],
                step_number=step_data["step_number"]
            )
            db.session.add(step)
    
    db.session.commit()
    logger.info("Sample remedies imported successfully")

def run_initialization():
    """Run the complete database initialization process"""
    logger.info("Starting database initialization...")
    
    # Create initial categories
    create_categories()
    
    # Create doctor accounts
    create_doctors()
    
    # Import sample data
    import_sample_plants()
    import_sample_remedies()
    
    logger.info("Database initialization completed successfully!")

if __name__ == "__main__":
    run_initialization()