# Use an official PHP runtime as a parent image
FROM php:7.4-apache

# Set working directory
WORKDIR /var/www/html

# Install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Copy local code to the container image
COPY . /var/www/html

# Use the PORT environment variable in Apache configuration files
RUN sed -i 's/80/8080/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# Configure Apache
RUN a2enmod rewrite

# Change the owner of the application inside the Docker image to fix potential permissions issues
RUN chown -R www-data:www-data /var/www/html

# Expose port 80 for the app
EXPOSE 8080

# Start Apache service
CMD ["apache2-foreground"]
