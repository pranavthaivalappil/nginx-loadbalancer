<<<<<<< HEAD
# Nginx Load Balancer

Dockerized Node.js application with Nginx load balancing across multiple instances.

## Features

Nginx distributes traffic across 3 Node.js instances using least-connection algorithm.
Real-time WebSocket chat demonstrates load distribution across backends.
HTTPS/SSL with automatic HTTP redirects and security headers.
Health monitoring with automatic failover for unhealthy instances.

## Installation

### Docker

```bash
docker-compose up --build
```

Access at https://localhost (HTTP redirects to HTTPS)

### Local Development

```bash
cd app
npm install
npm start
```

## Architecture

```
Client → Nginx (443) → app1:3000
                     → app2:3000
                     → app3:3000
```

## Configuration

### Load Balancing

Nginx uses `least_conn` algorithm in `nginx/nginx.conf`:

```nginx
upstream nodejs_backend {
    least_conn;
    server app1:3000 max_fails=3 fail_timeout=30s;
    server app2:3000 max_fails=3 fail_timeout=30s;
    server app3:3000 max_fails=3 fail_timeout=30s;
}
```

### Environment Variables

- `APP_NAME` - Instance identifier (app-1, app-2, app-3)
- `NODE_ENV` - Environment setting (development/production)

### SSL Certificates

Self-signed certificates in `nginx/ssl/`. For production, replace with valid certificates.

## License

[MIT License](LICENSE)
=======
Production-ready Node.js app with Nginx load balancing and Docker Compose
Nginx distributes traffic across multiple Node.js instances using least_conn.
HTTPS enabled with SSL, security headers, and health checks.
Real-time chat via Socket.io to visualize load distribution.
Easily scalable, containerized, and deployable on Vercel/Render/Railway.
>>>>>>> 3e6d1503978cb906e9aeeb0376bf76179e6d8d08
