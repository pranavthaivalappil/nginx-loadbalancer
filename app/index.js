const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

console.log('Starting server...');
console.log('PORT:', port);
console.log('NODE_ENV:', process.env.NODE_ENV);

// Health check endpoint
app.get('/api/health', (req, res) => {
    console.log('Health check request received');
    res.json({ status: 'OK', port: port, timestamp: Date.now() });
});

// Root endpoint
app.get('/', (req, res) => {
    console.log('Root request received');
    res.send(`
        <html>
            <head><title>Nginx Load Balancer</title></head>
            <body>
                <h1>🚀 Nginx Load Balancer Project</h1>
                <p>Server: railway-app</p>
                <p>Status: Running on port ${port}</p>
                <p>Time: ${new Date().toISOString()}</p>
                <a href="/api/health">Health Check</a>
            </body>
        </html>
    `);
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on port ${port}`);
    console.log(`Health check: http://localhost:${port}/api/health`);
});
