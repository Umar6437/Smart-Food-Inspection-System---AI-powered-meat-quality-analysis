"""Admin routes for dashboard and system management"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Analysis, AdminLog
from functools import wraps
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(f):
    """Decorator to check admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def log_admin_action(admin_id, action, details=None):
    """Log admin action"""
    try:
        log_entry = AdminLog(admin_id=admin_id, action=action, details=details)
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        print(f"Failed to log admin action: {e}")

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """Get admin dashboard stats"""
    try:
        user_id = get_jwt_identity()
        
        # Total users
        total_users = User.query.count()
        
        # Total analyses
        total_analyses = Analysis.query.count()
        
        # Recent analyses (last 24 hours)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_analyses = Analysis.query.filter(
            Analysis.created_at >= twenty_four_hours_ago
        ).count()
        
        # Average meat type confidence
        avg_meat_conf = db.session.query(
            db.func.avg(Analysis.meat_confidence)
        ).scalar() or 0.0
        
        # Average freshness confidence
        avg_fresh_conf = db.session.query(
            db.func.avg(Analysis.freshness_confidence)
        ).scalar() or 0.0
        
        # Top meat types
        top_meats = db.session.query(
            Analysis.meat_type,
            db.func.count(Analysis.id).label('count')
        ).group_by(Analysis.meat_type).order_by(db.desc('count')).limit(5).all()
        
        # Top freshness levels
        freshness_dist = db.session.query(
            Analysis.freshness,
            db.func.count(Analysis.id).label('count')
        ).group_by(Analysis.freshness).all()
        
        return jsonify({
            'total_users': total_users,
            'total_analyses': total_analyses,
            'recent_analyses_24h': recent_analyses,
            'avg_meat_confidence': float(avg_meat_conf),
            'avg_freshness_confidence': float(avg_fresh_conf),
            'top_meat_types': [{'name': m[0], 'count': m[1]} for m in top_meats],
            'freshness_distribution': [{'name': f[0], 'count': f[1]} for f in freshness_dist],
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Dashboard error: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """List all users"""
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        page = max(1, page)
        per_page = min(max(1, per_page), 100)
        
        paginated = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'data': [user.to_dict() for user in paginated.items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch users: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>/role', methods=['PATCH'])
@admin_required
def update_user_role(user_id):
    """Update user role"""
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'role' not in data:
            return jsonify({'error': 'Role required'}), 400
        
        new_role = data['role'].lower()
        if new_role not in ['user', 'admin']:
            return jsonify({'error': 'Invalid role. Must be user or admin'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        old_role = user.role
        user.role = new_role
        db.session.commit()
        
        # Log action
        log_admin_action(admin_id, 'update_user_role', f'User {user.email}: {old_role} -> {new_role}')
        
        return jsonify({
            'message': f'User role updated to {new_role}',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500

@admin_bp.route('/analyses', methods=['GET'])
@admin_required
def list_analyses():
    """List all analyses with filters"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        meat_type = request.args.get('meat_type', None)
        freshness = request.args.get('freshness', None)
        
        page = max(1, page)
        per_page = min(max(1, per_page), 100)
        
        query = Analysis.query
        
        if meat_type:
            query = query.filter_by(meat_type=meat_type)
        if freshness:
            query = query.filter_by(freshness=freshness)
        
        paginated = query.order_by(Analysis.created_at.desc()).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'data': [analysis.to_dict() for analysis in paginated.items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch analyses: {str(e)}'}), 500

@admin_bp.route('/system-health', methods=['GET'])
@admin_required
def system_health():
    """Get system health status"""
    try:
        # Database connectivity
        db_status = 'ok'
        try:
            db.session.execute('SELECT 1')
        except:
            db_status = 'error'
        
        # Count records
        user_count = User.query.count()
        analysis_count = Analysis.query.count()
        
        return jsonify({
            'status': 'healthy' if db_status == 'ok' else 'degraded',
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat(),
            'records': {
                'users': user_count,
                'analyses': analysis_count
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@admin_bp.route('/logs', methods=['GET'])
@admin_required
def get_logs():
    """Get admin activity logs"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        page = max(1, page)
        per_page = min(max(1, per_page), 100)
        
        paginated = AdminLog.query.order_by(AdminLog.created_at.desc()).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'data': [log.to_dict() for log in paginated.items]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch logs: {str(e)}'}), 500
