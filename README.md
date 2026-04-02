# 🏥 Health AI Predictor: Disease-Symptom Prediction System

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=render)](https://disease-prediction-miniproject.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Latest-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

An advanced, full-stack medical diagnostic tool using **Random Forest Machine Learning** to predict diseases based on symptoms and demographic data (Age, Gender). This project features a modern Glassmorphism UI, real-time precautions, and interactive data analytics.

---

## 🚀 [Live Application on Render](https://disease-prediction-miniproject.onrender.com)

---

## 🧠 Machine Learning Engine

### 🛠 Algorithm: Random Forest Classifier
The system uses a **Random Forest Classifier**, an ensemble learning method that provides robust accuracy by combining multiple decision trees.

- **Optimized Performance**: To ensure compatibility with low-resource environments (e.g., Render Free Tier), the model is optimized with **20 estimators** and a **max_depth of 25**.
- **Efficiency**: The total model footprint is only **0.30 MB** (compressed), making it lightweight and lightning-fast to load (<512MiB RAM usage).
- **Feature Engineering**: 
    - **Symptom Vectorization**: Uses `MultiLabelBinarizer` to convert comma-separated symptom lists into a 144-dimensional binary feature matrix.
    - **Demographic Integration**: Directly incorporates **Age** (integer) and **Gender** (Numeric Code) for high-fidelity predictions.

### 📊 Dataset Integration
Imerged three enterprise-grade datasets:
1. `Healthcare.csv`: Primary training data for symptom-disease mapping.
2. `DiseaseAndSymptoms.csv`: Supplementary source for broad symptom variety (17 symptom columns merged).
3. `Disease precaution.csv`: Mapping of diagnoses to immediate actionable medical advice.

---

## 💻 Tech Stack

### Backend
- **Core**: Python (Flask)
- **ML Framework**: Scikit-Learn, Joblib
- **Data Manipulation**: Pandas, NumPy
- **Server**: Gunicorn (WSGI)

### Frontend
- **Framework**: HTML5, CSS3 (Vanilla + Glassmorphism)
- **UI Components**: Bootstrap 5
- **Interactive Elements**: Select2 (Multi-select), FontAwesome
- **Visuals**: Chart.js (Interactive Pie & Bar charts)

---

## 🌟 Key Features

1. **AI-Powered Diagnostics**: Predicts diseases from a database of 40+ unique medical conditions.
2. **Actionable Insights**: Automatically fetches 4 specific **Medical Precautions** (Action Plans) for every prediction.
3. **Interactive Dashboard**: View top disease distributions and symptom frequencies in the "Analytics" tab.
4. **Demographic Input**: Adjusts results based on the patient's Age and Gender.
5. **Modern Experience**: Fully responsive, dark-mode themed "Glassmorphism" interface.

---

## 🛠 Installation & Local Setup

### 1. Prerequisite
Ensure you have Python 3.9+ installed.

### 2. Clone & Install
```bash
git clone https://github.com/DIWAKARDQ/Disease-prediction-miniproject.git
cd Disease-prediction-miniproject
pip install -r requirements.txt
```

### 3. Run the App
```bash
# Optional: Retrain the model
python train_model.py

# Start the Flask server
python app.py
```
Open `http://localhost:5000` in your browser.

---

## 📁 Repository Structure
```
.
├── Dataset/               # Original datasets (CSV)
├── static/                # CSS, JS, and Images
├── templates/             # HTML templates (JinJa2)
├── model.pkl              # Optimized Random Forest model
├── precautions.json       # Precaution lookup map
├── app.py                 # Flask Production Server
├── train_model.py         # ML Pipeline Script
└── Procfile               # Render Deployment Config
```

---

## ⚖ Disclaimer
*This project is for educational purposes only. The AI predictions are NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health providers with any questions you may have regarding a medical condition.*

---
**Developed by [DIWAKARDQ](https://github.com/DIWAKARDQ)**
