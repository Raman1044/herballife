from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for plant-benefit many-to-many relationship
plant_benefits = db.Table(
    'plant_benefits',
    Column('plant_id', Integer, ForeignKey('plant.id'), primary_key=True),
    Column('benefit_id', Integer, ForeignKey('benefit.id'), primary_key=True)
)

# Association table for remedy-benefit many-to-many relationship
remedy_benefits = db.Table(
    'remedy_benefits',
    Column('remedy_id', Integer, ForeignKey('remedy.id'), primary_key=True),
    Column('benefit_id', Integer, ForeignKey('benefit.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    name = Column(String(100))
    is_doctor = Column(Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.email}>"

class PlantCategory(db.Model):
    __tablename__ = 'plant_category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # Relationship with Plant
    plants = relationship("Plant", back_populates="category")
    
    def __repr__(self):
        return f"<PlantCategory {self.name}>"

class RemedyCategory(db.Model):
    __tablename__ = 'remedy_category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # Relationship with Remedy
    remedies = relationship("Remedy", back_populates="category")
    
    def __repr__(self):
        return f"<RemedyCategory {self.name}>"

class Benefit(db.Model):
    __tablename__ = 'benefit'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Benefit {self.name}>"

class Plant(db.Model):
    __tablename__ = 'plant'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    usage = Column(Text)
    category_id = Column(Integer, ForeignKey('plant_category.id'))
    
    # Relationships
    category = relationship("PlantCategory", back_populates="plants")
    images = relationship("PlantImage", back_populates="plant", cascade="all, delete-orphan")
    benefits = relationship("Benefit", secondary=plant_benefits)
    
    # For convenient access to the primary image
    @property
    def primary_image(self):
        if self.images:
            # Return the first image or one marked as primary if that feature is added
            return self.images[0].url
        return None
    
    def to_dict(self):
        """Convert plant object to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "category_info": {
                "id": self.category.id,
                "name": self.category.name
            } if self.category else None,
            "benefits": [benefit.name for benefit in self.benefits],
            "description": self.description,
            "usage": self.usage,
            "image": self.primary_image,
            "images": [image.url for image in self.images]
        }
    
    def __repr__(self):
        return f"<Plant {self.name}>"

class PlantImage(db.Model):
    __tablename__ = 'plant_image'
    
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plant.id'), nullable=False)
    url = Column(String(255), nullable=False)
    alt_text = Column(String(100))
    is_primary = Column(db.Boolean, default=False)
    
    # Relationship
    plant = relationship("Plant", back_populates="images")
    
    def __repr__(self):
        return f"<PlantImage {self.url} for plant {self.plant_id}>"

class Remedy(db.Model):
    __tablename__ = 'remedy'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    short_description = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, default="Medium")
    usage = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('remedy_category.id'))
    doctor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Relationships
    category = relationship("RemedyCategory", back_populates="remedies")
    ingredients = relationship("Ingredient", back_populates="remedy", cascade="all, delete-orphan")
    preparation_steps = relationship("PreparationStep", back_populates="remedy", cascade="all, delete-orphan")
    benefits = relationship("Benefit", secondary=remedy_benefits)
    doctor = relationship("User", backref="remedies")
    
    def to_dict(self):
        """Convert remedy object to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "short_description": self.short_description,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "category_info": {
                "id": self.category.id,
                "name": self.category.name
            } if self.category else None,
            "difficulty": self.difficulty,
            "ingredients": [ingredient.name for ingredient in self.ingredients],
            "description": self.description,
            "preparation_steps": [
                {"number": step.step_number, "description": step.description} 
                for step in sorted(self.preparation_steps, key=lambda x: x.step_number)
            ],
            "usage": self.usage,
            "benefits": [benefit.name for benefit in self.benefits],
            "doctor": {
                "id": self.doctor.id,
                "name": self.doctor.name,
                "is_doctor": self.doctor.is_doctor
            } if self.doctor else None
        }
    
    def __repr__(self):
        return f"<Remedy {self.name}>"

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    
    id = Column(Integer, primary_key=True)
    remedy_id = Column(Integer, ForeignKey('remedy.id'), nullable=False)
    name = Column(String(100), nullable=False)
    order = Column(Integer, default=0)  # For ordering ingredients in the list
    
    # Relationship
    remedy = relationship("Remedy", back_populates="ingredients")
    
    def __repr__(self):
        return f"<Ingredient {self.name} for remedy {self.remedy_id}>"

class PreparationStep(db.Model):
    __tablename__ = 'preparation_step'
    
    id = Column(Integer, primary_key=True)
    remedy_id = Column(Integer, ForeignKey('remedy.id'), nullable=False)
    description = Column(Text, nullable=False)
    step_number = Column(Integer, nullable=False)  # For ordering steps
    
    # Relationship
    remedy = relationship("Remedy", back_populates="preparation_steps")
    
    def __repr__(self):
        return f"<PreparationStep {self.step_number} for remedy {self.remedy_id}>"
