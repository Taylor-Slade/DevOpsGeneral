# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entrypoint script into the container and give execution rights
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the current directory contents into the container at /app
COPY . /app

# Install needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run unit tests (Optional - remove if you don't want to run tests during build)
RUN pytest

# Make port 5000 available outside this container
EXPOSE 5000

# Set the entrypoint to run the script using bash
ENTRYPOINT ["bash", "/entrypoint.sh"]

# Change to a non root user for security reasons
# USER non_root_user