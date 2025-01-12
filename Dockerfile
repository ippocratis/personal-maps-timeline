FROM php:8.1-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    git && \
    docker-php-ext-install pdo_mysql gettext

# Install other PHP extensions
RUN docker-php-ext-install mysqli

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

# Install Phinx globally via Composer
RUN composer global require robmorgan/phinx

# Set working directory
WORKDIR /var/www/html

# Mark the directory as safe for Git
RUN git config --global --add safe.directory /var/www/html

# Copy project files
COPY ./personal-maps-timeline /var/www/html

# Install project dependencies
#RUN composer clear-cache
#RUN composer update --prefer-source

# Expose port for PHP-FPM
# EXPOSE 9004

# Start PHP-FPM
CMD ["php-fpm"]
