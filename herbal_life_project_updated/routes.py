import logging
from flask import render_template, jsonify, request, abort, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import Plant, Remedy, PlantCategory, RemedyCategory, Benefit, Ingredient, PreparationStep, User, PlantImage

# Set up logging
logger = logging.getLogger(__name__)

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # If user is already logged in, redirect to home page
        if current_user.is_authenticated:
            return redirect(url_for('index'))
            
        # Process login form submission
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = 'remember' in request.form
            
            # Validate input
            if not email or not password:
                flash('Please enter both email and password', 'danger')
                return render_template('login.html')
                
            # Find the user
            user = User.query.filter_by(email=email).first()
            
            # Check if user exists and password is correct
            if user and user.check_password(password):
                login_user(user, remember=remember)
                flash('Login successful', 'success')
                
                # Redirect to the page user wanted to access before login if any
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
                
        # For GET requests, display the login form
        return render_template('login.html')
        
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # If user is already logged in, redirect to home page
        if current_user.is_authenticated:
            return redirect(url_for('index'))
            
        # Process registration form submission
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            is_doctor = 'is_doctor' in request.form
            
            # Validate input
            if not name or not email or not password or not confirm_password:
                flash('Please fill in all fields', 'danger')
                return render_template('register.html')
                
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return render_template('register.html')
                
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered. Please login or use a different email.', 'danger')
                return render_template('register.html')
                
            # Create new user
            user = User(email=email, name=name, is_doctor=is_doctor)
            user.set_password(password)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
            
        # For GET requests, display the registration form
        return render_template('register.html')
        
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('index'))
        
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')
    
    @app.route('/plants')
    def plants():
        return render_template('plants.html')
    
    @app.route('/remedies')
    def remedies():
        return render_template('remedies.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    # API Routes
    @app.route('/api/plants', methods=['GET'])
    def get_plants():
        try:
            # Get query parameters for filtering
            category = request.args.get('category')
            search = request.args.get('search')
            
            # Start with all plants query
            query = Plant.query
            
            # Apply filters if provided
            if category and category.lower() != 'all':
                query = query.join(Plant.category).filter(PlantCategory.name.ilike(f'%{category}%'))
            
            if search:
                search_term = f'%{search}%'
                query = query.filter(
                    (Plant.name.ilike(search_term)) | 
                    (Plant.scientific_name.ilike(search_term)) | 
                    (Plant.description.ilike(search_term))
                )
            
            # Execute the query
            plants = query.all()
            
            # Convert to dictionary format
            plants_dict = {"plants": [plant.to_dict() for plant in plants]}
            
            return jsonify(plants_dict)
        except Exception as e:
            logger.error(f"Error retrieving plants: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/plants/<int:plant_id>', methods=['GET'])
    def get_plant(plant_id):
        try:
            plant = Plant.query.get_or_404(plant_id)
            return jsonify(plant.to_dict())
        except Exception as e:
            logger.error(f"Error retrieving plant {plant_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/remedies', methods=['GET'])
    def get_remedies():
        try:
            # Get query parameters for filtering
            category = request.args.get('category')
            search = request.args.get('search')
            
            # Start with all remedies query
            query = Remedy.query
            
            # Apply filters if provided
            if category and category.lower() != 'all':
                query = query.join(Remedy.category).filter(RemedyCategory.name.ilike(f'%{category}%'))
            
            if search:
                search_term = f'%{search}%'
                query = query.filter(
                    (Remedy.name.ilike(search_term)) | 
                    (Remedy.description.ilike(search_term))
                )
                
                # Also search through ingredients (more complex query)
                ingredient_remedies = db.session.query(Remedy.id).join(
                    Ingredient, Ingredient.remedy_id == Remedy.id
                ).filter(Ingredient.name.ilike(search_term)).all()
                
                ingredient_remedy_ids = [r[0] for r in ingredient_remedies]
                
                if ingredient_remedy_ids:
                    query = query.union(Remedy.query.filter(Remedy.id.in_(ingredient_remedy_ids)))
            
            # Execute the query
            remedies = query.all()
            
            # Convert to dictionary format
            remedies_dict = {"remedies": [remedy.to_dict() for remedy in remedies]}
            
            return jsonify(remedies_dict)
        except Exception as e:
            logger.error(f"Error retrieving remedies: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/remedies/<int:remedy_id>', methods=['GET'])
    def get_remedy(remedy_id):
        try:
            remedy = Remedy.query.get_or_404(remedy_id)
            return jsonify(remedy.to_dict())
        except Exception as e:
            logger.error(f"Error retrieving remedy {remedy_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    # Admin API Routes for CRUD operations (these would normally be protected)
    @app.route('/api/plants', methods=['POST'])
    def create_plant():
        try:
            # Get data from request
            data = request.json
            
            # Find or create category
            category_name = data.get('category')
            category = PlantCategory.query.filter_by(name=category_name).first()
            if not category and category_name:
                category = PlantCategory(name=category_name)
                db.session.add(category)
            
            # Create new plant
            plant = Plant(
                name=data.get('name'),
                scientific_name=data.get('scientific_name'),
                description=data.get('description'),
                usage=data.get('usage'),
                category=category
            )
            
            # Add benefits
            for benefit_name in data.get('benefits', []):
                # Find or create benefit
                benefit = Benefit.query.filter_by(name=benefit_name).first()
                if not benefit:
                    benefit = Benefit(name=benefit_name)
                    db.session.add(benefit)
                plant.benefits.append(benefit)
            
            # Add images
            image_url = data.get('image')
            if image_url:
                plant.images.append(PlantImage(url=image_url, is_primary=True))
            
            # Add additional images
            for img_url in data.get('images', []):
                if img_url != image_url:  # Avoid duplicating the primary image
                    plant.images.append(PlantImage(url=img_url))
            
            # Save to database
            db.session.add(plant)
            db.session.commit()
            
            return jsonify(plant.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating plant: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/plants/<int:plant_id>', methods=['PUT'])
    def update_plant(plant_id):
        try:
            plant = Plant.query.get_or_404(plant_id)
            data = request.json
            
            # Update basic plant info
            if 'name' in data:
                plant.name = data['name']
            if 'scientific_name' in data:
                plant.scientific_name = data['scientific_name']
            if 'description' in data:
                plant.description = data['description']
            if 'usage' in data:
                plant.usage = data['usage']
            
            # Update category if provided
            if 'category' in data:
                category_name = data['category']
                category = PlantCategory.query.filter_by(name=category_name).first()
                if not category:
                    category = PlantCategory(name=category_name)
                    db.session.add(category)
                plant.category = category
            
            # Update benefits if provided
            if 'benefits' in data:
                # Clear existing benefits
                plant.benefits = []
                
                # Add new benefits
                for benefit_name in data['benefits']:
                    benefit = Benefit.query.filter_by(name=benefit_name).first()
                    if not benefit:
                        benefit = Benefit(name=benefit_name)
                        db.session.add(benefit)
                    plant.benefits.append(benefit)
            
            # Update image if provided
            if 'image' in data:
                # Remove existing primary image if any
                for image in plant.images:
                    if image.is_primary:
                        db.session.delete(image)
                
                # Add new primary image
                plant.images.append(PlantImage(url=data['image'], is_primary=True))
            
            # Update additional images if provided
            if 'images' in data:
                # Keep only the primary image
                primary_image = next((img for img in plant.images if img.is_primary), None)
                plant.images = [primary_image] if primary_image else []
                
                # Add the new images
                for img_url in data['images']:
                    # Skip if it's the same as the primary image
                    if primary_image and img_url == primary_image.url:
                        continue
                    plant.images.append(PlantImage(url=img_url))
            
            db.session.commit()
            return jsonify(plant.to_dict())
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating plant {plant_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        try:
            plant = Plant.query.get_or_404(plant_id)
            db.session.delete(plant)
            db.session.commit()
            return jsonify({"message": f"Plant {plant_id} deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting plant {plant_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/remedies', methods=['POST'])
    def create_remedy():
        try:
            # Get data from request
            data = request.json
            
            # Find or create category
            category_name = data.get('category')
            category = RemedyCategory.query.filter_by(name=category_name).first()
            if not category and category_name:
                category = RemedyCategory(name=category_name)
                db.session.add(category)
            
            # Create new remedy
            remedy = Remedy(
                name=data.get('name'),
                short_description=data.get('short_description'),
                description=data.get('description'),
                difficulty=data.get('difficulty', 'Medium'),
                usage=data.get('usage'),
                category=category
            )
            
            # Add ingredients
            for i, ingredient_name in enumerate(data.get('ingredients', [])):
                remedy.ingredients.append(Ingredient(name=ingredient_name, order=i))
            
            # Add preparation steps
            for i, step_text in enumerate(data.get('preparation_steps', [])):
                remedy.preparation_steps.append(PreparationStep(description=step_text, step_number=i+1))
            
            # Add benefits
            for benefit_name in data.get('benefits', []):
                # Find or create benefit
                benefit = Benefit.query.filter_by(name=benefit_name).first()
                if not benefit:
                    benefit = Benefit(name=benefit_name)
                    db.session.add(benefit)
                remedy.benefits.append(benefit)
            
            # Save to database
            db.session.add(remedy)
            db.session.commit()
            
            return jsonify(remedy.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating remedy: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/remedies/<int:remedy_id>', methods=['PUT'])
    def update_remedy(remedy_id):
        try:
            remedy = Remedy.query.get_or_404(remedy_id)
            data = request.json
            
            # Update basic remedy info
            if 'name' in data:
                remedy.name = data['name']
            if 'short_description' in data:
                remedy.short_description = data['short_description']
            if 'description' in data:
                remedy.description = data['description']
            if 'difficulty' in data:
                remedy.difficulty = data['difficulty']
            if 'usage' in data:
                remedy.usage = data['usage']
            
            # Update category if provided
            if 'category' in data:
                category_name = data['category']
                category = RemedyCategory.query.filter_by(name=category_name).first()
                if not category:
                    category = RemedyCategory(name=category_name)
                    db.session.add(category)
                remedy.category = category
            
            # Update ingredients if provided
            if 'ingredients' in data:
                # Remove all existing ingredients
                for ingredient in remedy.ingredients:
                    db.session.delete(ingredient)
                
                # Add new ingredients
                for i, ingredient_name in enumerate(data['ingredients']):
                    remedy.ingredients.append(Ingredient(name=ingredient_name, order=i))
            
            # Update preparation steps if provided
            if 'preparation_steps' in data:
                # Remove all existing steps
                for step in remedy.preparation_steps:
                    db.session.delete(step)
                
                # Add new steps
                for i, step_text in enumerate(data['preparation_steps']):
                    remedy.preparation_steps.append(PreparationStep(description=step_text, step_number=i+1))
            
            # Update benefits if provided
            if 'benefits' in data:
                # Clear existing benefits
                remedy.benefits = []
                
                # Add new benefits
                for benefit_name in data['benefits']:
                    benefit = Benefit.query.filter_by(name=benefit_name).first()
                    if not benefit:
                        benefit = Benefit(name=benefit_name)
                        db.session.add(benefit)
                    remedy.benefits.append(benefit)
            
            db.session.commit()
            return jsonify(remedy.to_dict())
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating remedy {remedy_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/remedies/<int:remedy_id>', methods=['DELETE'])
    def delete_remedy(remedy_id):
        try:
            remedy = Remedy.query.get_or_404(remedy_id)
            db.session.delete(remedy)
            db.session.commit()
            return jsonify({"message": f"Remedy {remedy_id} deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting remedy {remedy_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500
