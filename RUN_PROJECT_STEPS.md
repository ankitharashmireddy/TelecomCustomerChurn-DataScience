# Manual Installation and Run Guide

This guide provides step-by-step instructions to set up and run the Customer Churn Prediction application manually.

## Prerequisites
- Python 3.10 or higher
- Git (optional, for cloning)

## Installation Steps

1. **Clone the Repository** (if not already done):
   ```bash
   git clone https://github.com/ankitharashmireddy/TelecomCustomerChurn-DataScience.git
   cd "TelecomCustomerChurn-DataScience"
   ```

2. **Set up a Virtual Environment** (Recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and set a secure `SECRET_KEY`.
   ```bash
   copy .env.example .env
   ```

## Running the Application

### Option 1: Using the Batch File (Windows)
Simply double-click `Run_Project.bat` in the project root. This will automatically check for dependencies, ensure the model is present, and start the Flask server.

### Option 2: Manual Start
Run the following command in your terminal:
```bash
python app.py
```

After starting, the application will be available at:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Login Credentials
Use one of the following accounts to log in:

| Username | Password |
|---|---|
| AnkithaRashmiReddy | Reddy@123 |
| PawanSimhaR | Simha@123 |
| AsraFathima | Asra@123 |
