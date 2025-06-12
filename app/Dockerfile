# Base image for Python
FROM python:3.13-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose the port Flask app will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
