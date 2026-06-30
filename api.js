// API Configuration
const API_BASE_URL = 'http://localhost:5000';

class API {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        // Add authorization token if available
        const token = localStorage.getItem('authToken');
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    static register(email, password) {
        return this.request('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
    }

    static login(email, password) {
        return this.request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
    }

    static getProfile() {
        return this.request('/api/auth/profile');
    }

    static refreshToken() {
        return this.request('/api/auth/refresh', {
            method: 'POST',
        });
    }

    // Analysis
    static analyzeImage(imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);

        return this.request('/api/analyze', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
            },
            body: formData,
        });
    }

    static getHistory(page = 1, perPage = 20) {
        return this.request(`/api/history?page=${page}&per_page=${perPage}`);
    }

    static getAnalysisDetail(analysisId) {
        return this.request(`/api/history/${analysisId}`);
    }

    static getStats() {
        return this.request('/api/stats');
    }

    // Admin
    static getDashboard() {
        return this.request('/api/admin/dashboard');
    }

    static getUsers(page = 1, perPage = 20) {
        return this.request(`/api/admin/users?page=${page}&per_page=${perPage}`);
    }

    static updateUserRole(userId, role) {
        return this.request(`/api/admin/users/${userId}/role`, {
            method: 'PATCH',
            body: JSON.stringify({ role }),
        });
    }

    static getAnalyses(page = 1, perPage = 20, filters = {}) {
        let query = `/api/admin/analyses?page=${page}&per_page=${perPage}`;
        if (filters.meatType) query += `&meat_type=${filters.meatType}`;
        if (filters.freshness) query += `&freshness=${filters.freshness}`;
        return this.request(query);
    }

    static getSystemHealth() {
        return this.request('/api/admin/system-health');
    }

    static getAdminLogs(page = 1, perPage = 50) {
        return this.request(`/api/admin/logs?page=${page}&per_page=${perPage}`);
    }

    // Health Check
    static getHealth() {
        return this.request('/api/health');
    }
}
