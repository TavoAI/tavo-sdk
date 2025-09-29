const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Health check endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'Tavo.AI API Server',
        version: '1.0.0',
        status: 'healthy'
    });
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

app.listen(PORT, '127.0.0.1', () => {
    console.log(`Mock API server running on port ${PORT} (PID: ${process.pid})`);
    console.log(`Health check: http://127.0.0.1:${PORT}/`);
}).on('error', (err) => {
    console.error('Mock API failed to start:', err);
    process.exit(1);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('Mock API received SIGTERM, shutting down gracefully');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('Mock API received SIGINT, shutting down gracefully');
    process.exit(0);
});