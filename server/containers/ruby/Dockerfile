# Use an official Ruby runtime as a parent image
FROM ruby:3.0.1

# Set the working directory in the container to /app
WORKDIR /app

# Copy Gemfile and Gemfile.lock into the image
COPY Gemfile ./

# Install bundler and the gems from the Gemfile
RUN gem install bundler && bundle install

# Add your application to the image (ensure the .dockerignore file is set to ignore unnecessary files)
ADD . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# The command to run your application when the container is run. Replace "app.rb" with your filename.
CMD ["rerun", "app.rb", "-p", "8080", "-b", "0.0.0.0"]