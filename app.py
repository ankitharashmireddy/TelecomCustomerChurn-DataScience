from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pickle
import os
import sqlite3
from functools import wraps

# --- Configuration & Initialization ---
app = Flask(__name__)
# Load SECRET_KEY from environment, with a strong fallback only for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_change_in_production_12345')
csrf = CSRFProtect(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Seed default users
        default_users = {
            "AnkithaRashmiReddy": "Reddy@123",
            "PawanSimhaR": "Simha@123",
            "AsraFathima": "Asra@123"
        }
        for username, password in default_users.items():
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                           (username, generate_password_hash(password)))
        conn.commit()
        conn.close()

init_db()

# --- Feature Configuration ---
# Defining feature order once to ensure consistency between training and inference
FEATURE_ORDER = [
    'Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Tenure', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
]

# --- Model Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'churn_prediction_model.pkl')
model = None

print(f"[*] Attempting to load model from: {MODEL_PATH}")

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
            print("[+] Model loaded successfully!")
    except Exception as e:
        print(f"[!] CRITICAL: Error loading model: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"[!] CRITICAL: Model file NOT FOUND at {MODEL_PATH}")

# --- Security Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Security Headers ---
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# --- Routes ---

@app.route('/')
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and check_password_hash(result[0], password):
        session['user'] = username
        return redirect(url_for('index'))
    
    return render_template('login.html', error="Invalid username or password")

@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        if not model:
            return render_template("index.html", prediction_error="System Error: AI Model not available.")

        def sanitize_input(val, default=0.0):
            try:
                return float(val) if val else default
            except (ValueError, TypeError):
                return default

        # Process inputs maintainable and securely
        final_features = [sanitize_input(request.form.get(f)) for f in FEATURE_ORDER]
        
        # Inference with Probability for Confidence Score
        feature_array = np.array([final_features])
        prediction = model.predict(feature_array)[0]
        
        # Get probability if model supports it (VotingClassifier usually does)
        confidence = 0
        try:
            probabilities = model.predict_proba(feature_array)[0]
            confidence = np.max(probabilities) * 100
        except:
            confidence = 100 # Fallback if model doesn't support proba

        result = "Churn" if prediction == 1 else "No Churn"
        inputs = list(request.form.items())
        
        return render_template("result.html", 
                               inputs=inputs, 
                               prediction=result, 
                               confidence=round(confidence, 2))
    except Exception as e:
        return render_template("index.html", prediction_error=f"Prediction Encountered an Issue: {str(e)}")

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Production note: In real deployment, use Gunicorn/Nginx and disable debug
    app.run(host="0.0.0.0", port=5000, debug=False)