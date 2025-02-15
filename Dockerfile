# Use a minimal Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . /app

# Expose the port for FastAPI
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "fastapi_pereval.main:app", "--host", "0.0.0.0", "--port", "8000"]