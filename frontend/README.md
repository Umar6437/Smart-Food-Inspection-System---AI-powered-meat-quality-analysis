# Smart Food Inspection System - Frontend

A modern, responsive web application for analyzing meat quality using AI/ML predictions.

## Features

- **User Authentication** - Secure login and registration
- **Image Upload & Analysis** - Drag & drop interface for image analysis
- **Real-time Predictions** - Instant meat type and freshness detection
- **History Tracking** - View all previous analyses
- **User Statistics** - Track analysis trends and data
- **Admin Dashboard** - System monitoring and user management
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Modern UI** - Clean, intuitive interface with smooth animations

## Project Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Styling and animations
├── js/
│   ├── api.js          # API client and requests
│   └── app.js          # Main application logic
└── README.md           # This file
```

## Installation & Setup

### Prerequisites
- Backend server running on `http://localhost:5000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

1. **Open in Browser**
   ```bash
   # Simply open index.html in your browser
   # Or use a local server
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

2. **Configure Backend URL** (if needed)
   - Edit `js/api.js`
   - Change `API_BASE_URL` to match your backend URL
   ```javascript
   const API_BASE_URL = 'http://localhost:5000';
   ```

## Features Explained

### Authentication
- **Register** - Create new user account
- **Login** - Secure login with JWT tokens
- **Profile** - View account information

### Image Analysis
- **Upload** - Drag & drop or click to upload images
- **Analysis** - Real-time meat quality detection
- **Results** - View meat type, freshness, and confidence scores
- **Safety Recommendation** - Get consumption recommendations

### History & Statistics
- **View History** - See all previous analyses
- **Statistics** - Track meat types and freshness trends
- **Date Filter** - Sort by analysis date

### Admin Dashboard
- **User Management** - View and manage users
- **System Monitoring** - Check system health and status
- **Analytics** - View system-wide statistics
- **Recent Analyses** - Monitor recent analysis data

## API Integration

The frontend communicates with the backend API using the `API` class in `js/api.js`.

### Key Methods

```javascript
// Authentication
API.login(email, password)
API.register(email, password)
API.getProfile()

// Analysis
API.analyzeImage(imageFile)
API.getHistory(page, perPage)
API.getStats()

// Admin
API.getDashboard()
API.getUsers(page, perPage)
API.getAnalyses(page, perPage, filters)
```

## Demo Credentials

### Regular User
- **Email:** user@example.com
- **Password:** password123

### Admin User
- **Email:** admin@example.com
- **Password:** adminpass123

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox and grid
- **JavaScript (ES6+)** - Client-side logic
- **Fetch API** - HTTP requests to backend
- **Font Awesome** - Icon library

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Responsive Design

- Desktop: Full-width layout
- Tablet: Optimized grid layouts
- Mobile: Single column, touch-friendly

## Key CSS Variables

```css
--primary-color: #2ecc71 (Green)
--secondary-color: #3498db (Blue)
--danger-color: #e74c3c (Red)
--warning-color: #f39c12 (Orange)
--dark-bg: #2c3e50
--light-bg: #ecf0f1
```

## Performance Optimizations

- Lazy loading of images
- Debounced API calls
- Cached user authentication
- Efficient DOM manipulation
- Minimized animations

## Security Features

- JWT token-based authentication
- Secure password storage (backend)
- CORS enabled for frontend
- XSS protection with proper escaping
- CSRF token support (can be added)

## Future Enhancements

- [ ] Image gallery with drag reorder
- [ ] Export analysis results as PDF
- [ ] Email notifications
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Advanced filtering and search
- [ ] Batch image upload
- [ ] Real-time collaboration

## Troubleshooting

### "API Connection Failed"
- Ensure backend is running on `http://localhost:5000`
- Check CORS is enabled on backend
- Verify network connectivity

### "Login Not Working"
- Check that registered user exists
- Verify backend authentication endpoints
- Check browser console for errors

### "Images Not Uploading"
- Check file size (max 16MB)
- Verify supported formats (JPG, PNG, GIF, BMP, WebP)
- Check backend file upload settings

## Support

For issues or questions:
1. Check browser console (F12) for errors
2. Review backend logs
3. Verify API endpoints are working
4. Check network tab in developer tools

## License

MIT License - Feel free to use and modify

## Author

Smart Food Inspection System Team

## Version

1.0.0 - Initial Release
