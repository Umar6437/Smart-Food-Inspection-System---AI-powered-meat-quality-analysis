// Application State
const state = {
    isAuthenticated: false,
    currentUser: null,
    currentPage: 'home',
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
});

function initializeApp() {
    console.log('Initializing Smart Food Inspection System...');
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    if (token) {
        loadUserProfile();
    }
}

// Event Listeners Setup
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = e.target.dataset.page;
            navigateTo(page);
        });
    });

    // Auth Modal
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const authModal = document.getElementById('authModal');
    const closeModal = document.getElementById('closeAuthModal');
    const switchToRegister = document.getElementById('switchToRegister');
    const switchToLogin = document.getElementById('switchToLogin');

    if (loginBtn) loginBtn.addEventListener('click', () => openAuthModal('login'));
    if (logoutBtn) logoutBtn.addEventListener('click', logout);
    if (closeModal) closeModal.addEventListener('click', closeAuthModal);
    if (switchToRegister) switchToRegister.addEventListener('click', (e) => {
        e.preventDefault();
        showAuthForm('register');
    });
    if (switchToLogin) switchToLogin.addEventListener('click', (e) => {
        e.preventDefault();
        showAuthForm('login');
    });

    // Auth Forms
    document.getElementById('loginFormElement').addEventListener('submit', handleLogin);
    document.getElementById('registerFormElement').addEventListener('submit', handleRegister);

    // Upload Area
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const uploadBtn = document.getElementById('uploadBtn');

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageSelect(files[0]);
        }
    });

    uploadBtn.addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageSelect(e.target.files[0]);
        }
    });

    // Get Started Button
    document.getElementById('getStartedBtn').addEventListener('click', () => {
        if (state.isAuthenticated) {
            navigateTo('analyze');
        } else {
            openAuthModal('login');
        }
    });
}

// Navigation
function navigateTo(page) {
    // Check if page requires authentication
    const protectedPages = ['analyze', 'history', 'profile', 'admin'];
    if (protectedPages.includes(page) && !state.isAuthenticated) {
        openAuthModal('login');
        return;
    }

    // Check if admin page requires admin role
    if (page === 'admin' && state.currentUser?.role !== 'admin') {
        showToast('You do not have admin access', 'error');
        return;
    }

    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.style.display = 'none');

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === page) {
            link.classList.add('active');
        }
    });

    // Show selected page
    const pageElement = document.getElementById(`${page}Page`);
    if (pageElement) {
        pageElement.style.display = 'block';
        state.currentPage = page;

        // Load page-specific data
        if (page === 'history') loadHistory();
        if (page === 'profile') loadProfile();
        if (page === 'admin') loadAdminDashboard();
    }
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    showLoading(true);
    try {
        const data = await API.login(email, password);
        localStorage.setItem('authToken', data.access_token);
        state.isAuthenticated = true;
        state.currentUser = data.user;
        updateAuthUI();
        closeAuthModal();
        showToast('Login successful!', 'success');
        navigateTo('home');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    if (password !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }

    showLoading(true);
    try {
        const data = await API.register(email, password);
        localStorage.setItem('authToken', data.access_token);
        state.isAuthenticated = true;
        state.currentUser = data.user;
        updateAuthUI();
        closeAuthModal();
        showToast('Registration successful!', 'success');
        navigateTo('home');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function loadUserProfile() {
    try {
        const data = await API.getProfile();
        state.currentUser = data;
        state.isAuthenticated = true;
        updateAuthUI();
    } catch (error) {
        console.error('Failed to load profile:', error);
        logout();
    }
}

function updateAuthUI() {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const adminLink = document.getElementById('adminLink');

    if (state.isAuthenticated) {
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'block';
        if (state.currentUser?.role === 'admin') {
            adminLink.style.display = 'block';
        }
    } else {
        loginBtn.style.display = 'block';
        logoutBtn.style.display = 'none';
        adminLink.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('authToken');
    state.isAuthenticated = false;
    state.currentUser = null;
    updateAuthUI();
    showToast('Logged out successfully', 'success');
    navigateTo('home');
}

function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    if (token) {
        loadUserProfile();
    }
}

// Auth Modal Functions
function openAuthModal(form = 'login') {
    const authModal = document.getElementById('authModal');
    showAuthForm(form);
    authModal.style.display = 'block';
}

function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
    document.getElementById('loginFormElement').reset();
    document.getElementById('registerFormElement').reset();
}

function showAuthForm(form) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (form === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// Image Analysis
async function handleImageSelect(file) {
    // Validate file
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showToast('File size exceeds 16MB limit', 'error');
        return;
    }

    // Preview image
    const reader = new FileReader();
    reader.onload = (e) => {
        const imagePreview = document.getElementById('imagePreview');
        const previewImage = document.getElementById('previewImage');
        previewImage.src = e.target.result;
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    // Analyze image
    showLoading(true);
    try {
        const prediction = await API.analyzeImage(file);
        displayAnalysisResult(prediction);
        showToast('Analysis completed!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displayAnalysisResult(prediction) {
    const meatConfidencePercent = Math.round(prediction.meat_confidence * 100);
    const freshnessConfidencePercent = Math.round(prediction.freshness_confidence * 100);

    document.getElementById('meatType').textContent = prediction.meat_type;
    document.getElementById('meatConfidence').style.width = `${meatConfidencePercent}%`;
    document.getElementById('meatConfidencePercent').textContent = meatConfidencePercent;

    document.getElementById('freshnessLevel').textContent = prediction.freshness;
    document.getElementById('freshnessConfidence').style.width = `${freshnessConfidencePercent}%`;
    document.getElementById('freshnessConfidencePercent').textContent = freshnessConfidencePercent;

    // Generate safety recommendation
    let safetyText = '';
    if (prediction.freshness === 'fresh') {
        safetyText = '✓ Safe to consume. Meat appears fresh with good quality.';
    } else if (prediction.freshness === 'moderate') {
        safetyText = '⚠ Use with caution. Meat is moderately fresh. Consume soon or refrigerate properly.';
    } else {
        safetyText = '✗ Not recommended. Meat shows signs of spoilage. Do not consume.';
    }

    document.getElementById('safetyText').textContent = safetyText;
    document.getElementById('analysisResult').style.display = 'block';
}

// History Page
async function loadHistory() {
    const historyContainer = document.getElementById('historyContainer');
    historyContainer.innerHTML = '<div class="loader">Loading history...</div>';

    try {
        const historyData = await API.getHistory();
        const statsData = await API.getStats();

        // Display stats
        document.getElementById('totalAnalyses').textContent = statsData.total_analyses;
        document.getElementById('recentAnalyses').textContent = statsData.recent_analyses_7d;
        document.getElementById('historyStats').style.display = 'grid';

        // Display history items
        if (historyData.data.length === 0) {
            historyContainer.innerHTML = '<p style="text-align: center; padding: 2rem;">No analysis history yet.</p>';
        } else {
            historyContainer.innerHTML = historyData.data.map(item => `
                <div class="history-item">
                    <div class="history-image">
                        <img src="https://via.placeholder.com/150" alt="Analysis">
                    </div>
                    <div class="history-info">
                        <div class="history-info-item">
                            <h4>Meat Type</h4>
                            <p>${item.meat_type}</p>
                        </div>
                        <div class="history-info-item">
                            <h4>Freshness</h4>
                            <p>${item.freshness}</p>
                        </div>
                        <div class="history-info-item">
                            <h4>Date</h4>
                            <p>${new Date(item.created_at).toLocaleDateString()}</p>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        historyContainer.innerHTML = `<p style="text-align: center; padding: 2rem; color: red;">Error loading history: ${error.message}</p>`;
    }
}

// Profile Page
function loadProfile() {
    if (state.currentUser) {
        document.getElementById('userEmail').textContent = state.currentUser.email;
        document.getElementById('userRole').textContent = state.currentUser.role;
        document.getElementById('userJoinDate').textContent = new Date(state.currentUser.created_at).toLocaleDateString();
    }
}

// Admin Dashboard
async function loadAdminDashboard() {
    try {
        const dashboard = await API.getDashboard();
        const health = await API.getSystemHealth();
        const users = await API.getUsers();
        const analyses = await API.getAnalyses();

        // Update dashboard cards
        document.getElementById('totalUsers').textContent = dashboard.total_users;
        document.getElementById('totalAnalysesAdmin').textContent = dashboard.total_analyses;
        document.getElementById('recentAnalysesAdmin').textContent = dashboard.recent_analyses_24h;
        document.getElementById('systemHealth').textContent = health.status.toUpperCase();

        // Display users table
        const usersTable = `
            <table>
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Joined</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.data.map(user => `
                        <tr>
                            <td>${user.email}</td>
                            <td>${user.role}</td>
                            <td>${new Date(user.created_at).toLocaleDateString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('usersTableContainer').innerHTML = usersTable;

        // Display analyses table
        const analysesTable = `
            <table>
                <thead>
                    <tr>
                        <th>Meat Type</th>
                        <th>Freshness</th>
                        <th>Confidence</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    ${analyses.data.slice(0, 10).map(analysis => `
                        <tr>
                            <td>${analysis.meat_type}</td>
                            <td>${analysis.freshness}</td>
                            <td>${Math.round(analysis.meat_confidence * 100)}%</td>
                            <td>${new Date(analysis.created_at).toLocaleDateString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('analysesTableContainer').innerHTML = analysesTable;
    } catch (error) {
        showToast('Failed to load admin dashboard: ' + error.message, 'error');
    }
}

// Utility Functions
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.style.display = 'flex';
    } else {
        spinner.style.display = 'none';
    }
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const authModal = document.getElementById('authModal');
    if (e.target === authModal) {
        closeAuthModal();
    }
});
