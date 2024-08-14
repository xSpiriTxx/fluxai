FROM python:3.9-slim

WORKDIR /app

# Copy the FastAPI app code
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
