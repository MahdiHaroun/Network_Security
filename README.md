# 🛡️ Network Security Project

> **AI-powered phishing detection system with automated ML workflows and intelligent monitoring**

A machine learning-powered phishing detection system with automated workflows for network security analysis.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)](https://mongodb.com)
[![MLflow](https://img.shields.io/badge/MLflow-%23d9ead3.svg?style=flat&logo=numpy&logoColor=blue)](https://mlflow.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=flat&logo=amazon-s3&logoColor=white)](https://aws.amazon.com/s3/)
[![N8N](https://img.shields.io/badge/N8N-EA4B71?style=flat&logo=n8n&logoColor=white)](https://n8n.io)

## Overview

This project detects phishing attempts using machine learning models. It includes:
- **FastAPI web application** for predictions
- **Automated ML pipeline** for training models
- **N8N automation workflow** for intelligent processing
- **Docker containerization** for easy deployment
- **AWS ECR integration** for cloud deployment
- **MLflow tracking** for experiment monitoring and model versioning
- **DAGs monitoring** with comprehensive experiment tracking

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
- **Saves results to MongoDB and S3
- **Sends notifications on completion
- **Monitored with MLflow for experiment tracking

**Benefits:**
- No manual intervention needed
- Automatic error handling
- Scheduled processing
- Real-time monitoring
- Comprehensive experiment tracking with DAGs

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
- **MLflow Tracking**: Experiment monitoring with DAGs for ML pipeline oversight
- **API Endpoints**: RESTful APIs for predictions and data upload

## Author

**Mahdi Haroun** - mhd0228222@ju.edu.jo

---

*For detailed technical documentation, check the code comments in each module.*