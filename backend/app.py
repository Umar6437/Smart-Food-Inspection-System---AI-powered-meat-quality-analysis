"""
Smart Food Inspection System - Flask Backend
Main application factory and initialization
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    """Application factory"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, 'development'))
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))
    JWTManager(app)
    
    # Register blueprints
    from auth import auth_bp
    from analysis import analysis_bp
    from admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(admin_bp)
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Smart Food Inspection System',
            'version': '1.0.0'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database initialized")
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
