# Use official Node.js image as base
FROM node:20-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build the frontend for production (uncomment if you want a production build)
# RUN npm run build

# Expose the port the dev server runs on
EXPOSE 8080

# Start the development server by default
CMD ["npm", "run", "serve"]
