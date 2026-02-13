FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-fastapi.txt .
RUN pip install --no-cache-dir -r requirements-fastapi.txt

# Copy application code
COPY main.py .
COPY storage.py .
COPY yle_utils.py .
COPY custom_fleep/ ./custom_fleep/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
