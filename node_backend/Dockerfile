# Use Node.js LTS version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy only package files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy rest of the code
COPY . .

# Expose backend port
EXPOSE 3000

# Start the server
CMD ["npm", "start"]
