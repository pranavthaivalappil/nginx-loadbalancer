const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

const appName = process.env.APP_NAME || 'local-server';

// Serve static files (images, CSS, JS)
app.use('/images', express.static(path.join(__dirname, 'images')));
app.use(express.static(path.join(__dirname, 'public')));

// API routes for load balancing demo
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        app: appName,
        timestamp: new Date().toISOString()
    });
    console.log(`Health check served by ${appName}`);
});

app.get('/api/info', (req, res) => {
    res.json({
        message: 'Hello from Node.js server!',
        app: appName,
        timestamp: new Date().toISOString()
    });
    console.log(`Info request served by ${appName}`);
});

// Main route
app.use('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
    console.log(`Request served by ${appName}`);
});

//Chat application
const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

io.on('connection', (socket) => {
    console.log(`User connected to ${appName}`);
    
    socket.on('message', (data) => {
        io.emit('message', {
            ...data,
            server: appName,
            timestamp: new Date().toISOString()
        });
        console.log(`Message handled by ${appName}: ${data.text}`);
    });

    socket.on('disconnect', () => {
        console.log(`User disconnected from ${appName}`);
    });
});

server.listen(port, () => {
    console.log(`${appName} is listening on port ${port}`);
});