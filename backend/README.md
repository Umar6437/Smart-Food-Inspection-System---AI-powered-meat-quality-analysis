# Smart Food Inspection System - Flask Backend

A Flask-based REST API for meat quality inspection and analysis using AI/ML predictions.

## Features

- **User Authentication**: Register, login, JWT token-based authentication
- **Image Analysis**: Upload meat images for freshness and type classification
- **History Tracking**: Store and retrieve analysis history for authenticated users
- **Admin Dashboard**: System monitoring, user management, analytics
- **Database**: SQLAlchemy ORM with SQLite (development) or PostgreSQL (production)
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Mock ML Model**: Simulated meat inspection predictions (ready to integrate real models)

## Project Structure

```
backend/
├── app.py              # Flask application factory
├── config.py           # Configuration for different environments
├── models.py           # Database models (User, Analysis, AdminLog)
├── auth.py             # Authentication endpoints
├── analysis.py         # Image analysis endpoints
├── admin.py            # Admin management endpoints
├── ml_model.py         # ML model for predictions (mock implementation)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Installation

### 1. Clone and Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Initialize Database

```bash
python setup_db.py
```

## Running the Server

### Development

```bash
python app.py
# or with Flask CLI
flask run
```

Server runs on `http://localhost:5000`

### Production

```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (requires JWT)
- `POST /api/auth/refresh` - Refresh access token (requires JWT)

### Analysis

- `POST /api/analyze` - Analyze meat image (returns predictions)
- `GET /api/history` - Get user analysis history (requires JWT)
- `GET /api/history/<id>` - Get specific analysis (requires JWT)
- `GET /api/stats` - Get user statistics (requires JWT)

### Admin (requires admin role)

- `GET /api/admin/dashboard` - Dashboard stats
- `GET /api/admin/users` - List all users
- `PATCH /api/admin/users/<id>/role` - Update user role
- `GET /api/admin/analyses` - List all analyses (filterable)
- `GET /api/admin/system-health` - System health status
- `GET /api/admin/logs` - Admin activity logs

### Health

- `GET /api/health` - Service health check

## Example Usage

### Register and Login

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"securepass"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"securepass"}'
```

### Analyze Image

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@/path/to/meat_image.jpg" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get History

```bash
curl -X GET http://localhost:5000/api/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Configuration

Edit `.env` to customize:

- `FLASK_ENV` - `development` or `production`
- `SECRET_KEY` - Flask secret (change in production!)
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - JWT signing key (change in production!)
- `CORS_ORIGINS` - Allowed frontend origins

## Admin Access

For demo purposes, any user with "admin" in their email becomes an admin:

```bash
# Register as admin
{
  "email": "admin@example.com",
  "password": "adminpass"
}
```

## ML Model Integration

The `ml_model.py` contains a mock implementation. To integrate real models:

1. Train/export your TensorFlow, PyTorch, or scikit-learn model
2. Load in `MeatInspectionModel.__init__()`
3. Implement real feature extraction in `_analyze_image_features()`
4. Replace mock predictions in `predict()`

Example:

```python
import tensorflow as tf

class MeatInspectionModel:
    def __init__(self, model_version='1.0'):
        self.model = tf.keras.models.load_model('trained_meat_model.h5')
    
    def predict(self, image_bytes):
        # Process image, run inference
        predictions = self.model.predict(...)
        return predictions
```

## Database

### Models

- **User**: Email, password hash, role (user/admin), timestamps
- **Analysis**: Image metadata, predictions, confidence scores, user reference
- **AdminLog**: Admin actions and timestamps

### Migrations

For production, use Alembic:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Security Notes

⚠️ **For Production**:

1. Change `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`
2. Use PostgreSQL instead of SQLite
3. Enable HTTPS only
4. Implement rate limiting
5. Use environment-specific CORS origins
6. Add input validation and sanitization
7. Implement proper logging
8. Regular security audits

## Testing

Create `test_app.py`:

```python
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
```

Run: `pytest`

## Troubleshooting

### Port already in use
```bash
lsof -i :5000
kill -9 <PID>
# Or use different port
flask run --port 5001
```

### Database locked
```bash
rm sfis_dev.db
```

### Import errors
```bash
pip install -e .
```

## Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit: `git commit -m 'Add amazing feature'`
3. Push: `git push origin feature/amazing-feature`
4. Open Pull Request

## License

MIT

## Support

For issues, open a GitHub issue or contact support.
