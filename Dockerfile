# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with Uvicorn
#CMD ["uvicorn", "Bilstm_api:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "Bilstm_api:app", "--host", "localhost", "--port", "8000"]