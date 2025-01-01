# Use an official base image from Docker Hub
FROM ubuntu:latest

# Set environment variables (optional)
ENV APP_HOME /app

# Install any dependencies (optional)
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR $APP_HOME

# Copy application files from your local machine to the Docker image
COPY . .

# Expose port (optional, depending on your app)
EXPOSE 80

# Define the command to run when the container starts
CMD ["python3", "app.py"]

