# Use the official node image as a base
FROM node:18-slim

# Set a working directory for the application
WORKDIR /app

# Copy the package.json file
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application files
COPY . .

# Expose the port your application runs on
EXPOSE 3000

# Start the application
CMD [ "npm", "start", "--host", "0.0.0.0" ]
