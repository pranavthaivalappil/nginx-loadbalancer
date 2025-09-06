# Use official Node.js runtime as base image
FROM node:18-alpine

# Set working directory in container
WORKDIR /usr/src/app

# Copy package files
COPY app/package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy application code
COPY app/ .

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]