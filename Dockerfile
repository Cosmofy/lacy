# Use official Python image
FROM python:latest

# Set working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi strawberry-graphql redis httpx uvicorn

# Expose the port for FastAPI
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]