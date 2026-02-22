#!/bin/bash

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies for document processing
sudo apt install tesseract-ocr -y
sudo apt install poppler-utils -y
sudo apt install ffmpeg -y
sudo apt install espeak espeak-data libespeak1 libespeak-dev -y

# Install git
sudo apt install git -y

# Install nginx (optional, for reverse proxy)
sudo apt install nginx -y

# Install supervisor for process management
sudo apt install supervisor -y

echo "System setup completed!"