"""
Script to import doctor-recommended Ayurvedic remedies into the database
"""
import logging
from app import app, db
from models import Remedy, RemedyCategory, Benefit, Ingredient, PreparationStep, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_doctor(name, email, password):
    """Create a doctor user if they don't already exist"""
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        logger.info(f"Doctor {name} already exists in database")
        return existing_user
        
    # Create new doctor user
    user = User(
        name=name,
        email=email,
        is_doctor=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    logger.info(f"Created doctor: {name}")
    return user

def create_remedy_category(name):
    """Create remedy category if it doesn't exist"""
    category = RemedyCategory.query.filter_by(name=name).first()
    if not category:
        category = RemedyCategory(name=name)
        db.session.add(category)
        db.session.commit()
        logger.info(f"Created remedy category: {name}")
    return category

def create_benefit(name):
    """Create benefit if it doesn't exist"""
    benefit = Benefit.query.filter_by(name=name).first()
    if not benefit:
        benefit = Benefit(name=name)
        db.session.add(benefit)
        db.session.commit()
        logger.info(f"Created benefit: {name}")
    return benefit

def import_doctor_remedies():
    """Import doctor-recommended remedies into the database"""
    
    # Create remedy categories
    traditional_cat = create_remedy_category("Traditional Ayurvedic Remedies")
    digestive_cat = create_remedy_category("Digestive Health Remedies")
    immunity_cat = create_remedy_category("Immunity Boosting Remedies")
    stress_cat = create_remedy_category("Stress Relief Remedies")
    inflammation_cat = create_remedy_category("Anti-inflammatory Preparations")
    
    # Create doctors
    dr_chopra = create_doctor(
        "Dr. Deepak Chopra", 
        "deepak.chopra@example.com", 
        "securepassword123"
    )
    
    dr_lad = create_doctor(
        "Dr. Vasant Lad", 
        "vasant.lad@example.com", 
        "securepassword123"
    )
    
    dr_frawley = create_doctor(
        "Dr. David Frawley", 
        "david.frawley@example.com", 
        "securepassword123"
    )
    
    # List of remedies to be imported
    remedies_data = [
        {
            "name": "Ginger Tea for Digestive Health",
            "doctor": dr_chopra,
            "category": digestive_cat,
            "short_description": "A soothing ginger tea that helps improve digestion and reduce bloating.",
            "description": "This classic Ayurvedic remedy uses the power of fresh ginger to stimulate digestion and relieve common digestive issues like gas and bloating. Recommended by Dr. Deepak Chopra for maintaining digestive health.",
            "difficulty": "Easy",
            "usage": "Drink warm, preferably before or after meals. Can be consumed 1-2 times daily.",
            "ingredients": [
                "1-inch fresh ginger root (grated or sliced)",
                "2 cups water",
                "1 tsp honey (optional)",
                "1/2 tsp lemon juice (optional)"
            ],
            "preparation_steps": [
                "Boil 2 cups of water in a saucepan.",
                "Add the grated/sliced ginger and let it simmer for 5–10 minutes.",
                "Strain the tea into a cup.",
                "Add honey and lemon juice if desired."
            ],
            "benefits": [
                "Relieves gas and bloating",
                "Improves digestion",
                "Reduces inflammation"
            ]
        },
        {
            "name": "Tulsi Tea for Cold & Flu",
            "doctor": dr_lad,
            "category": immunity_cat,
            "short_description": "A healing tea made with holy basil (tulsi) to fight cold and flu symptoms.",
            "description": "Tulsi (Holy Basil) is revered in Ayurveda for its powerful healing properties, especially for respiratory conditions. Dr. Vasant Lad recommends this simple tea for strengthening immunity and relieving cold and flu symptoms.",
            "difficulty": "Easy",
            "usage": "Drink warm 2-3 times a day during cold and flu season or when experiencing symptoms.",
            "ingredients": [
                "5–6 fresh tulsi (holy basil) leaves",
                "1 cup water",
                "1/2 tsp honey (optional)",
                "1/4 tsp black pepper (optional)"
            ],
            "preparation_steps": [
                "Boil the tulsi leaves in 1 cup of water for 5 minutes.",
                "Strain and pour into a cup.",
                "Add honey and black pepper if desired."
            ],
            "benefits": [
                "Strengthens immunity",
                "Relieves cough and congestion",
                "Fights viral infections"
            ]
        },
        {
            "name": "Triphala Powder for Digestion & Detox",
            "doctor": dr_lad,
            "category": digestive_cat,
            "short_description": "A traditional formula using three fruits that support digestive health and detoxification.",
            "description": "Triphala is one of the most famous formulations in Ayurveda, consisting of three fruits: Amalaki, Bibhitaki, and Haritaki. Dr. Vasant Lad recommends this remedy for gentle cleansing and improving digestive function.",
            "difficulty": "Easy",
            "usage": "Take before bed on an empty stomach. Not recommended during pregnancy.",
            "ingredients": [
                "1 tsp Triphala powder",
                "1 cup warm water"
            ],
            "preparation_steps": [
                "Mix 1 tsp of Triphala powder in warm water.",
                "Stir well and drink before bed."
            ],
            "benefits": [
                "Supports digestion",
                "Detoxifies the body",
                "Promotes regular elimination",
                "Cleanses the colon"
            ]
        },
        {
            "name": "Ashwagandha Milk for Stress & Energy",
            "doctor": dr_frawley,
            "category": stress_cat,
            "short_description": "A nourishing milk preparation with ashwagandha to reduce stress and increase vitality.",
            "description": "Ashwagandha is known as the premier adaptogenic herb in Ayurveda. Dr. David Frawley recommends this nourishing milk preparation to help the body resist stress and build energy, particularly beneficial for those experiencing burnout or fatigue.",
            "difficulty": "Easy",
            "usage": "Drink before bedtime for relaxation and improved sleep. Can be consumed regularly for long-term benefits.",
            "ingredients": [
                "1 tsp Ashwagandha powder",
                "1 cup warm milk (dairy or plant-based)",
                "1/2 tsp honey (optional)",
                "1/4 tsp cinnamon (optional)"
            ],
            "preparation_steps": [
                "Warm a cup of milk.",
                "Add Ashwagandha powder and stir well.",
                "Add honey or cinnamon if desired."
            ],
            "benefits": [
                "Reduces stress and anxiety",
                "Boosts strength and stamina",
                "Improves sleep quality",
                "Supports hormonal balance"
            ]
        },
        {
            "name": "Turmeric Golden Milk for Inflammation & Immunity",
            "doctor": dr_frawley,
            "category": inflammation_cat,
            "short_description": "A warming golden milk that harnesses turmeric's anti-inflammatory properties.",
            "description": "Turmeric has been used for thousands of years in Ayurvedic medicine for its powerful anti-inflammatory and immune-boosting properties. Dr. David Frawley recommends this golden milk recipe as a daily tonic for reducing inflammation and supporting overall health.",
            "difficulty": "Easy",
            "usage": "Drink before bed for better immunity and anti-inflammatory benefits. Can be consumed daily as a preventative tonic.",
            "ingredients": [
                "1 cup milk (dairy or plant-based)",
                "1/2 tsp turmeric powder",
                "1/4 tsp black pepper",
                "1/2 tsp honey (optional)"
            ],
            "preparation_steps": [
                "Warm the milk in a saucepan.",
                "Add turmeric and black pepper. Stir well.",
                "Add honey for sweetness."
            ],
            "benefits": [
                "Reduces joint pain and inflammation",
                "Strengthens immunity",
                "Supports liver function",
                "Improves skin health"
            ]
        }
    ]
    
    # Import remedies into database
    for remedy_data in remedies_data:
        # Check if remedy already exists
        existing_remedy = Remedy.query.filter_by(name=remedy_data["name"]).first()
        if existing_remedy:
            logger.info(f"Remedy '{remedy_data['name']}' already exists, skipping")
            continue
            
        # Create new remedy
        remedy = Remedy(
            name=remedy_data["name"],
            short_description=remedy_data["short_description"],
            description=remedy_data["description"],
            difficulty=remedy_data["difficulty"],
            usage=remedy_data["usage"],
            category=remedy_data["category"],
            doctor=remedy_data["doctor"]  # Set doctor association
        )
        
        # Add ingredients
        for i, ingredient_name in enumerate(remedy_data["ingredients"]):
            remedy.ingredients.append(Ingredient(name=ingredient_name, order=i))
            
        # Add preparation steps
        for i, step_text in enumerate(remedy_data["preparation_steps"]):
            remedy.preparation_steps.append(PreparationStep(description=step_text, step_number=i+1))
            
        # Add benefits
        for benefit_name in remedy_data["benefits"]:
            benefit = create_benefit(benefit_name)
            remedy.benefits.append(benefit)
            
        # Save to database
        db.session.add(remedy)
        db.session.commit()
        logger.info(f"Added remedy: {remedy.name}")
    
    logger.info("Completed importing doctor-recommended remedies")

if __name__ == "__main__":
    with app.app_context():
        import_doctor_remedies()