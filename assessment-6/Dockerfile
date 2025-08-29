# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all source files
COPY . .

# Install dependencies
RUN pip install flask mysql-connector-python

# Expose port Flask will run on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app
CMD ["flask", "run"]
