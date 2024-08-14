FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the model server code
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the model server
CMD ["python3", "serve_model.py"]
