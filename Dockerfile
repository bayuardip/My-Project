FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update -y && \
    apt-get install -y libgl1-mesa-glx wget libglib2.0-0 curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Manually install npm
RUN apt-get install -y npm

# Verify Node.js and npm installation
RUN node --version && npm --version

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire application code
COPY . .

# Replace the existing title and noscript tags and inject the new meta tags
RUN sed -i 's|<title>.*</title>|<title>Market Mage</title>|' /usr/local/lib/python3.11/site-packages/streamlit/static/index.html
