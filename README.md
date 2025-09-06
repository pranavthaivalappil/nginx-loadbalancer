# 🚀 Nginx Load Balancer with Docker

A production-ready Node.js application demonstrating load balancing, containerization, and real-time communication.

## ✨ Features

- **Load Balancing**: Nginx distributes traffic across 3 Node.js instances
- **Docker Containerization**: Multi-container setup with Docker Compose
- **HTTPS/SSL**: Secure connections with self-signed certificates
- **Real-time Chat**: WebSocket communication showing load distribution
- **Health Monitoring**: Built-in health checks for all services
- **Production Ready**: Security headers, error handling, and logging

## 🏗️ Architecture

```
Internet → Nginx (Load Balancer) → Node.js App Instance 1
                                 → Node.js App Instance 2  
                                 → Node.js App Instance 3
```

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/pranavthaivalappil/nginx-loadbalancer.git
cd nginx-loadbalancer

# Start single instance for development
cd app
npm install
npm start
```

### Docker Deployment
```bash
# Build and run all services
docker-compose up --build

# Access the application
# HTTP: http://localhost (redirects to HTTPS)
# HTTPS: https://localhost
```

## 📁 Project Structure

```
├── app/
│   ├── server.js          # Node.js Express server with Socket.io
│   ├── package.json       # Dependencies and scripts
│   └── public/
│       └── index.html     # Frontend with chat interface
├── nginx/
│   ├── nginx.conf         # Load balancer configuration
│   └── ssl/               # SSL certificates
├── docker-compose.yaml    # Multi-service orchestration
├── Dockerfile            # Container configuration
└── README.md
```

## 🔧 Configuration

### Load Balancing Algorithm
- **Method**: `least_conn` (routes to server with fewest connections)
- **Health Checks**: Automatic failover if server becomes unhealthy
- **SSL Termination**: Nginx handles HTTPS encryption

### Environment Variables
- `APP_NAME`: Unique identifier for each instance (app-1, app-2, app-3)
- `NODE_ENV`: Environment setting (development/production)

## 🌐 Live Demo

🔗 **[View Live Application](https://your-app-url.railway.app)**

Try the real-time chat to see which server instance handles each message!

## 💡 Key Technologies

- **Backend**: Node.js, Express.js, Socket.io
- **Load Balancer**: Nginx
- **Containerization**: Docker, Docker Compose
- **Security**: HTTPS/SSL, Security Headers
- **Real-time**: WebSocket communication

## 🎯 Learning Outcomes

This project demonstrates:
- Container orchestration with Docker Compose
- Reverse proxy and load balancing with Nginx
- Real-time communication with WebSocket
- SSL/TLS certificate management
- Health monitoring and failover
- Production-ready security configurations

## 📊 Performance Features

- **Gzip Compression**: Reduced payload sizes
- **Connection Pooling**: Efficient resource usage
- **Health Checks**: Automatic server monitoring
- **Graceful Shutdowns**: Clean container stops

## 🔒 Security Features

- **HTTPS Redirect**: All traffic forced to secure connections
- **Security Headers**: XSS protection, HSTS, frame options
- **SSL/TLS**: Modern encryption protocols (TLS 1.2+)
- **Non-root User**: Containers run with limited privileges

## 📈 Scaling

The application can be easily scaled by:
- Adding more Node.js instances in `docker-compose.yaml`
- Updating the `upstream` block in `nginx.conf`
- Horizontal scaling on cloud platforms

## 🚀 Deployment

This project is deployed on Railway with automatic builds from GitHub.

### Deploy Your Own
1. Fork this repository
2. Connect to Railway
3. Deploy with one click!

## 👨‍💻 Author

**Pranav Vinod Thaivalappil**
- GitHub: [@pranavthaivalappil](https://github.com/pranavthaivalappil)
- LinkedIn: [pranav-thaivalappil](https://linkedin.com/in/pranav-thaivalappil/)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
