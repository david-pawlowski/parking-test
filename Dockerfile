# Use the official Python image as the base image
FROM python:3

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project to the container
COPY . .

# Collect static files (if applicable)
# RUN python manage.py collectstatic --noinput

# Run the Django development server (adjust this command as needed)
CMD python manage.py runserver 0.0.0.0:8000
