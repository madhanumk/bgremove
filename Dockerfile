# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY . /app/

# Expose the port that Django will run on (default 8000)
EXPOSE 8000

# Run the application
CMD ["gunicorn", "bgremove.wsgi:application", "--bind", "0.0.0.0:8000"]
