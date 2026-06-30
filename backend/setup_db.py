#!/usr/bin/env python
"""Database setup and initialization script"""

from app import create_app, db
from models import User, Analysis, AdminLog

def init_db():
    """Initialize database with tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Check if seed data exists
        if User.query.first() is None:
            print("\nAdding seed data...")
            
            # Create demo users
            demo_user = User(email='user@example.com', role='user')
            demo_user.set_password('password123')
            
            demo_admin = User(email='admin@example.com', role='admin')
            demo_admin.set_password('adminpass123')
            
            db.session.add(demo_user)
            db.session.add(demo_admin)
            db.session.commit()
            
            print("✓ Demo users created:")
            print("  - user@example.com (role: user)")
            print("  - admin@example.com (role: admin)")
        else:
            print("Database already contains data")
        
        print("\n✓ Database initialization complete!")
        print("\nDevelopment server: python app.py")
        print("Health check: http://localhost:5000/api/health")

if __name__ == '__main__':
    init_db()
