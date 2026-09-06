# Telecom Customer Churn Prediction

A machine learning-powered web application that predicts whether a telecom customer will churn based on their account details, service subscriptions, and billing information. Built with Flask, scikit-learn, and an ensemble of advanced ML models.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [ML Pipeline](#ml-pipeline)
- [Getting Started](#getting-started)
- [Login Credentials](#login-credentials)
- [Application Screenshots](#application-screenshots)
- [Model Details](#model-details)
- [Security Features](#security-features)
- [Authors](#authors)
- [License](#license)

---

## Project Overview

Customer churn is one of the biggest challenges in the telecom industry. Acquiring a new customer costs significantly more than retaining an existing one. This project uses machine learning to predict whether a customer is likely to leave (churn) based on 19 features spanning personal info, services subscribed, and billing details.

The prediction model is an **Ensemble Voting Classifier** combining four powerful algorithms:
- **Random Forest Classifier**
- **XGBoost Classifier**
- **LightGBM Classifier**
- **CatBoost Classifier**

The web app is built with **Flask**, features a **multi-step form** UI for easy data entry, and includes **user authentication** with a SQLite database.

---

## Key Features

- **Ensemble ML Model** — Combines 4 classifiers for high-accuracy predictions with confidence scores
- **Multi-Step Form** — Clean 3-step wizard UI for entering customer data (Personal Info → Services → Billing)
- **User Authentication** — Login system with hashed passwords and session management
- **CSRF Protection** — Form security via Flask-WTF
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, XSS Protection, HSTS
- **Result Download** — Download prediction results as an image (PNG) via html2canvas
- **Responsive Design** — Mobile-friendly UI with modern CSS styling
- **Confidence Score** — Displays prediction probability for informed decision-making

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, JavaScript |
| **ML Libraries** | scikit-learn, XGBoost, LightGBM, CatBoost, imbalanced-learn (SMOTE) |
| **Data Processing** | pandas, NumPy |
| **Database** | SQLite |
| **Security** | Flask-WTF (CSRF), Werkzeug (password hashing), Security Headers |
| **Visualization** | seaborn, matplotlib (Notebook EDA) |

---

## Project Structure

```
TelecomCustomerChurn-DataScience/
|
|-- app.py                              # Flask web application (routes, auth, prediction)
|-- database_setup.py                   # Standalone script to initialize the SQLite DB
|-- churn_prediction_model.pkl          # Pre-trained ensemble ML model (~84 MB)
|-- IT_customer_churn.csv               # Customer churn dataset
|-- Customer Churn Analysis and Prediction.ipynb  # Jupyter Notebook (EDA + Model Training)
|-- requirements.txt                    # Python dependencies
|-- .env.example                        # Environment variable template
|-- RUN_PROJECT_STEPS.md                # Step-by-step manual run guide
|-- LICENSE                             # MIT License
|
|-- templates/                          # Jinja2 HTML templates
|   |-- login.html                      #   Login page with password toggle
|   |-- index.html                      #   Multi-step prediction form
|   |-- result.html                     #   Prediction result display
|
|-- static/                             # Static assets
|   |-- style.css                       #   Global stylesheet
|   |-- Background.jpg                  #   Background image
|   |-- Churn.jpg                       #   Logo/favicon image
|   |-- Churn.ico                       #   Favicon (ICO format)
|
|-- users.db                            # SQLite database (auto-created)
|-- ChrunPrediction/                    # (Empty, excluded via .gitignore)
```

---

## Dataset

**File:** `IT_customer_churn.csv`

The dataset contains **7,043 rows** and **21 columns** representing telecom customer data with the following features:

### Input Features (19)

| # | Feature | Type | Description |
|---|---------|------|-------------|
| 1 | Gender | Categorical | Male / Female |
| 2 | SeniorCitizen | Binary | Whether the customer is a senior citizen (0/1) |
| 3 | Partner | Binary | Whether the customer has a partner |
| 4 | Dependents | Binary | Whether the customer has dependents |
| 5 | Tenure | Numeric | Number of months the customer has been with the company |
| 6 | PhoneService | Binary | Whether the customer has phone service |
| 7 | MultipleLines | Categorical | No phone service / No / Yes |
| 8 | InternetService | Categorical | No / DSL / Fiber optic |
| 9 | OnlineSecurity | Categorical | No internet service / No / Yes |
| 10 | OnlineBackup | Categorical | No internet service / No / Yes |
| 11 | DeviceProtection | Categorical | No internet service / No / Yes |
| 12 | TechSupport | Categorical | No internet service / No / Yes |
| 13 | StreamingTV | Categorical | No internet service / No / Yes |
| 14 | StreamingMovies | Categorical | No internet service / No / Yes |
| 15 | Contract | Categorical | Month-to-month / One year / Two year |
| 16 | PaperlessBilling | Binary | Whether the customer uses paperless billing |
| 17 | PaymentMethod | Categorical | Electronic check / Mailed check / Bank transfer / Credit card |
| 18 | MonthlyCharges | Numeric | Monthly billing amount ($) |
| 19 | TotalCharges | Numeric | Total amount charged to the customer ($) |

### Target Variable

| Feature | Description |
|---------|-------------|
| Churn | Whether the customer churned (Yes/No) |

---

## ML Pipeline

The Jupyter Notebook (`Customer Churn Analysis and Prediction.ipynb`) covers the full ML workflow:

### 1. Data Loading & Exploration
- Loaded `IT_customer_churn.csv` (7,043 rows x 21 columns)
- Checked data types, null values, and statistical summaries
- Explored class distribution of the target variable

### 2. Data Preprocessing
- **Label Encoding** — Converted all categorical columns to numeric
- **Type Conversion** — Converted `TotalCharges`, `MonthlyCharges`, and `Tenure` to numeric (handling errors)
- **Missing Values** — Dropped null values after conversion
- **Feature Scaling** — Applied `StandardScaler` for normalization

### 3. Exploratory Data Analysis (EDA)
- **Distribution Plots** — Histograms with KDE for Tenure, MonthlyCharges, TotalCharges
- **Count Plots** — Bar charts for all categorical features (Gender, Partner, PhoneService, InternetService, Contract, etc.)
- **Churn Analysis** — Visualized churn distribution across features

### 4. Handling Class Imbalance
- Applied **SMOTE (Synthetic Minority Over-sampling Technique)** to balance the churn/non-churn classes in the training data

### 5. Model Training
Four individual classifiers were trained with optimized hyperparameters:

| Model | Key Parameters |
|-------|---------------|
| **Random Forest** | n_estimators=500, max_depth=15, min_samples_split=5, min_samples_leaf=2, class_weight='balanced' |
| **XGBoost** | n_estimators=500, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=3 |
| **LightGBM** | n_estimators=500, max_depth=8, learning_rate=0.1, num_leaves=50, class_weight='balanced' |
| **CatBoost** | iterations=500, depth=8, learning_rate=0.1, verbose=0 |

### 6. Ensemble (Final Model)
- Combined all four models using **VotingClassifier** (soft voting)
- Final predictions based on averaged probability scores

### 7. Evaluation
- **Accuracy Score** — Overall model accuracy on test set
- **Classification Report** — Precision, Recall, F1-Score per class
- **Confusion Matrix** — True/False Positives and Negatives

### 8. Model Export
- Serialized the trained ensemble model as `churn_prediction_model.pkl` using Python's `pickle`

---

## Getting Started

### Prerequisites
- **Python 3.10+**
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ankitharashmireddy/TelecomCustomerChurn-DataScience.git
   cd TelecomCustomerChurn-DataScience
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set a secure `SECRET_KEY`. Generate one with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Login Credentials

The application requires authentication. Use one of the pre-configured accounts:

| Username | Password |
|----------|----------|
| AnkithaRashmiReddy | Reddy@123 |
| PawanSimhaR | Simha@123 |
| AsraFathima | Asra@123 |

> The primary default account is **AnkithaRashmiReddy**. User credentials are stored as hashed passwords in the SQLite database (`users.db`), which is auto-created on first run.

---

## Application Screenshots

### Login Page
Secure login with password visibility toggle and CSRF protection.

### Prediction Form
3-step wizard:
- **Step 1** — Personal & Account Info (Gender, Senior Citizen, Partner, Dependents, Tenure)
- **Step 2** — Services (Phone Service, Multiple Lines, Internet Service, Online Security, etc.)
- **Step 3** — Billing & Payment (Streaming, Contract, Paperless Billing, Payment Method, Monthly/Total Charges)

### Result Page
Displays the prediction (Churn / No Churn) with a confidence score and a summary table of all input features. Results can be downloaded as a PNG image.

---

## Model Details

| Metric | Value |
|--------|-------|
| **Algorithm** | Ensemble Voting Classifier (Soft Voting) |
| **Base Models** | Random Forest, XGBoost, LightGBM, CatBoost |
| **Balancing Technique** | SMOTE |
| **Feature Scaling** | StandardScaler |
| **Total Features** | 19 input features |
| **Model Size** | ~84 MB |
| **Serialization** | Python pickle |

---

## Security Features

- **Password Hashing** — Werkzeug's `generate_password_hash` / `check_password_hash` (PBKDF2)
- **CSRF Protection** — Flask-WTF CSRF tokens on all forms
- **Session Management** — Server-side Flask sessions with secure cookies
- **Login Required Decorator** — Protected routes redirect unauthenticated users
- **Security Headers:**
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: SAMEORIGIN`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- **Input Sanitization** — All form inputs sanitized before model inference

---

## Authors

| Name | GitHub | LinkedIn | Email |
|------|--------|----------|-------|
| **Ankitha Rashmi Reddy** | [ankitharashmireddy](https://github.com/ankitharashmireddy) | [Ankitha Rashmi Reddy](https://www.linkedin.com/in/ankitha-rashmi-reddy/) | ankitharashmireddy@gmail.com |

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

> Built with passion for data science and machine learning. Contributions, issues, and feature requests are welcome!
