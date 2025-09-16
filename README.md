# Network Security Project

A machine learning-powered phishing detection system with automated workflows for network security analysis.

## Overview

This project detects phishing attempts using machine learning models. It includes:
- **FastAPI web application** for predictions
- **Automated ML pipeline** for training models
- **N8N automation workflow** for intelligent processing
- **Docker containerization** for easy deployment
- **AWS ECR integration** for cloud deployment

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app:app --reload
```

### Docker Deployment
```bash
# Build the Docker image
docker build -t network-security-app .

# Run the container
docker run -p 8000:8000 network-security-app
```

## N8N Automation Agent

The project includes an N8N workflow (`N8N Agent/PredectionAgent.json`) that automates the entire prediction process:

**What it does:**
- Monitors for new data uploads
- Automatically validates CSV files
- Triggers predictions on valid data
- Saves results to MongoDB and S3


## AWS ECR Deployment

The project is containerized and ready for AWS ECR:

```bash
# 1. Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com

# 2. Tag the image
docker tag network-security-app:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/network-security-app:latest

# 3. Push to ECR
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/network-security-app:latest
```

## Project Structure

```
├── app.py                    # FastAPI application
├── main.py                   # ML training pipeline
├── Dockerfile               # Container configuration
├── N8N Agent/               # Automation workflow
├── Network_Security/        # Core ML package
├── final_model/            # Trained models
└── prediction_output/      # Results storage
```

## Environment Setup

Create a `.env` file with:
```
MONGODB_PASSWORD=your_mongodb_password
```

## Features

- **Phishing Detection**: ML-based URL and content analysis
- **Data Validation**: Automatic CSV validation and cleaning
- **Cloud Storage**: Integration with AWS S3 for data storage
- **Monitoring**: Comprehensive logging and error tracking
- **API Endpoints**: RESTful APIs for predictions and data upload

## Author

**Mahdi Haroun** - mhd0228222@ju.edu.jo

---

*For detailed technical documentation, check the code comments in each module.*