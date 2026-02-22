#!/bin/bash

# Create application directory
sudo mkdir -p /opt/dataspark
cd /opt/dataspark

# Clone or copy your application files
# If using git: git clone your-repo-url .
# For now, we'll assume files are copied manually

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/uploads
mkdir -p data/audio
mkdir -p generated_images
mkdir -p images/extracted

# Set permissions
sudo chown -R ubuntu:ubuntu /opt/dataspark
chmod +x *.sh

echo "Application setup completed!"