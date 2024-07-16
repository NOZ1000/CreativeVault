# Use Nginx base image
FROM nginx:latest

# Remove default nginx configuration file
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy nginx configuration file
COPY nginx.conf /etc/nginx/conf.d

# Copy the built Vue.js app into the nginx public directory
COPY dist/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
