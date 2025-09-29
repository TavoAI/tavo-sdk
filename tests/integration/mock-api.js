const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());
app.use((req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
});

// Mock API endpoints that SDKs expect
app.post('/api/v1/scan', (req, res) => {
    const { code, language } = req.body;

    // Mock scan result
    const mockResult = {
        scan_id: `scan_${Date.now()}`,
        total_issues: Math.floor(Math.random() * 5),
        issues: [],
        language: language || 'unknown',
        status: 'completed'
    };

    res.json(mockResult);
});

app.get('/api/v1/health', (req, res) => {
    res.json({ status: 'healthy', version: '1.0.0' });
});

app.post('/api/v1/auth/test', (req, res) => {
    const authHeader = req.headers['x-api-key'] || req.headers['authorization'];

    if (!authHeader) {
        return res.status(401).json({ error: 'No authentication provided' });
    }

    res.json({ authenticated: true, user: 'test-user' });
});

// WebSocket endpoint for real-time updates (simplified)
app.get('/ws', (req, res) => {
    res.json({ message: 'WebSocket endpoint available' });
});

app.listen(PORT, () => {
    console.log(`Mock API server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/api/v1/health`);
});