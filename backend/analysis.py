"""Analysis and prediction routes"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User, Analysis
import os
from ml_model import get_model
from datetime import datetime, timedelta

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_or_guest():
    """Get current user or return None for guest"""
    try:
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None

@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    """Analyze meat image"""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: JPG, PNG, GIF, BMP, WebP'}), 400
        
        # Read file data
        file_data = file.read()
        
        if len(file_data) > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large (max 16MB)'}), 413
        
        # Run ML model
        model = get_model()
        prediction = model.predict(file_data)
        
        # Save to database if user is authenticated
        user = get_user_or_guest()
        if user:
            analysis = Analysis(
                user_id=user.id,
                image_filename=secure_filename(file.filename),
                meat_type=prediction['meat_type'],
                meat_confidence=prediction['meat_confidence'],
                freshness=prediction['freshness'],
                freshness_confidence=prediction['freshness_confidence'],
                model_version=prediction['model_version'],
                processing_time_ms=prediction['processing_time_ms']
            )
            db.session.add(analysis)
            db.session.commit()
        
        return jsonify(prediction), 200
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@analysis_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Get analysis history for authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Ensure reasonable pagination
        page = max(1, page)
        per_page = min(max(1, per_page), 100)
        
        # Query analyses
        query = Analysis.query.filter_by(user_id=user.id).order_by(Analysis.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'data': [analysis.to_dict() for analysis in paginated.items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch history: {str(e)}'}), 500

@analysis_bp.route('/history/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis_detail(analysis_id):
    """Get specific analysis detail"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        analysis = Analysis.query.filter_by(id=analysis_id, user_id=user.id).first()
        
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify(analysis.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch analysis: {str(e)}'}), 500

@analysis_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Total analyses
        total_analyses = Analysis.query.filter_by(user_id=user.id).count()
        
        # Meat type distribution
        meat_types = db.session.query(
            Analysis.meat_type,
            db.func.count(Analysis.id).label('count')
        ).filter_by(user_id=user.id).group_by(Analysis.meat_type).all()
        
        # Freshness distribution
        freshness_levels = db.session.query(
            Analysis.freshness,
            db.func.count(Analysis.id).label('count')
        ).filter_by(user_id=user.id).group_by(Analysis.freshness).all()
        
        # Last 7 days trend
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_analyses = Analysis.query.filter_by(user_id=user.id).filter(
            Analysis.created_at >= seven_days_ago
        ).count()
        
        return jsonify({
            'total_analyses': total_analyses,
            'recent_analyses_7d': recent_analyses,
            'meat_type_distribution': {item[0]: item[1] for item in meat_types},
            'freshness_distribution': {item[0]: item[1] for item in freshness_levels}
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500
