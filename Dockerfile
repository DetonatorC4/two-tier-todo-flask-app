# Set Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy code
COPY . .

# Install app dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Serve app
CMD ["python", "app.py"]