const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

const appName = process.env.APP_NAME || 'railway-app';

console.log(`Starting ${appName} on port ${port}`);

// Basic middleware
app.use(express.static(path.join(__dirname, 'public')));

// Health check - MUST work for Railway
app.get('/api/health', (req, res) => {
    console.log(`Health check served by ${appName}`);
    res.status(200).json({
        status: 'healthy',
        app: appName,
        timestamp: new Date().toISOString(),
        port: port
    });
});

// API info endpoint
app.get('/api/info', (req, res) => {
    console.log(`Info request served by ${appName}`);
    res.status(200).json({
        message: 'Hello from Node.js server!',
        app: appName,
        timestamp: new Date().toISOString()
    });
});

// Main route
app.get('/', (req, res) => {
    console.log(`Main page request served by ${appName}`);
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(port, '0.0.0.0', () => {
    console.log(`${appName} is listening on port ${port}`);
    console.log(`Health check available at: http://localhost:${port}/api/health`);
});

// Error handling
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});
