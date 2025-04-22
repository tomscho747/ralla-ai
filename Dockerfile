# Use Python 3.10 base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the application files
COPY app.py /app/

# Copy the model file into the container
COPY moondream-0_5b-int8.mf /app/

# Install dependencies
RUN pip install flask pillow moondream

# Expose port 5000
EXPOSE 5000

# Use JSON array for CMD (recommended by Docker linter)
CMD ["python", "app.py"]
