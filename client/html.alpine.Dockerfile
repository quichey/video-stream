# Use a Node.js base image
FROM node:alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json ./
COPY package-lock.json ./

# Install application dependencies
RUN npm install

# Copy the rest of the application code
COPY . ./

# Build the React application for production
RUN npm run build

# Use a lightweight Nginx image to serve the built static files
FROM nginx:alpine

# Copy the built React app from the previous stage to Nginx's HTML directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 for the Nginx server
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]