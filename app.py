from flask import Flask, render_template, request, jsonify
import joblib
import json
import os
import numpy as np

app = Flask(__name__)

# Load the trained model and features
MODEL_PATH = 'model.pkl'
FEATURES_PATH = 'features.pkl'
ANALYTICS_PATH = 'analytics_data.json'
PRECAUTIONS_PATH = 'precautions.json'

model = None
features = []
precautions = {}

if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    print(f"Loaded model and {len(features)} features.")
else:
    print("Warning: Model or features not found. Please run train_model.py first.")

if os.path.exists(PRECAUTIONS_PATH):
    with open(PRECAUTIONS_PATH, 'r') as f:
        precautions = json.load(f)
    print(f"Loaded precautions for {len(precautions)} diseases.")
else:
    print("Warning: Precautions not found.")

@app.route('/')
def home():
    # Exclude demographics from the symptoms dropdown
    display_symptoms = [f for f in features if f not in ['Age', 'Gender_Code']]
    return render_template('index.html', symptoms=display_symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not features:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
        
    try:
        data = request.json
        selected_symptoms = data.get('symptoms', [])
        age = data.get('age')
        gender = data.get('gender')
        
        if not selected_symptoms:
            return jsonify({'error': 'No symptoms provided.'}), 400
            
        if not age or not str(age).isdigit():
            return jsonify({'error': 'Please provide a valid age.'}), 400
            
        if not gender in ['Male', 'Female', 'Other']:
            return jsonify({'error': 'Please provide a valid gender.'}), 400
            
        # Create input array of zeros
        input_data = np.zeros(len(features))
        
        age = int(age)
        gender_code = {'Male': 0, 'Female': 1, 'Other': 2}.get(gender, 2)
        
        # Populate Age and Gender_Code dynamically if they exist in training features
        if 'Age' in features:
            input_data[features.index('Age')] = age
        if 'Gender_Code' in features:
            input_data[features.index('Gender_Code')] = gender_code
        
        # Set 1 for selected symptoms
        for symptom in selected_symptoms:
            if symptom in features:
                index = features.index(symptom)
                input_data[index] = 1
                
        # Make prediction
        prediction = model.predict([input_data])[0]
        
        # Get precautions for the predicted disease
        disease_precautions = precautions.get(prediction.strip().title(), [])
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'precautions': disease_precautions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def analytics():
    analytics_data = {}
    if os.path.exists(ANALYTICS_PATH):
        with open(ANALYTICS_PATH, 'r') as f:
            analytics_data = json.load(f)
    return render_template('analytics.html', data=analytics_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render gives PORT
    app.run(host="0.0.0.0", port=port)