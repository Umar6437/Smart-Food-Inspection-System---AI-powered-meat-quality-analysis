from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class Analysis(db.Model):
    """Analysis/prediction model"""
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Input
    image_filename = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True)  # Store small thumbnails or metadata
    
    # Predictions
    meat_type = db.Column(db.String(50), nullable=False)
    meat_confidence = db.Column(db.Float, nullable=False)
    freshness = db.Column(db.String(50), nullable=False)  # 'fresh', 'moderate', 'spoiled'
    freshness_confidence = db.Column(db.Float, nullable=False)
    
    # Metadata
    model_version = db.Column(db.String(20), default='1.0', nullable=False)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meat_type': self.meat_type,
            'meat_confidence': float(self.meat_confidence),
            'freshness': self.freshness,
            'freshness_confidence': float(self.freshness_confidence),
            'model_version': self.model_version,
            'processing_time_ms': self.processing_time_ms,
            'created_at': self.created_at.isoformat()
        }

class AdminLog(db.Model):
    """Admin activity log"""
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action': self.action,
            'details': self.details,
            'created_at': self.created_at.isoformat()
        }
