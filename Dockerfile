# Start from the base Python 3.6 image
FROM python:3.6  

# Set the working directory inside the container
WORKDIR /app  

# Copy project files to the container
COPY . /app  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000  

# Default command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
