import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import json
import os

if __name__ == '__main__':
    print("Starting model training process...")

    # 1. Load Healthcare.csv
    healthcare_path = 'Dataset/Healthcare.csv'
    if not os.path.exists(healthcare_path):
        print(f"Error: Dataset not found at {healthcare_path}")
        exit(1)
        
    df_hc = pd.read_csv(healthcare_path)
    df_hc = df_hc.dropna(subset=['Disease'])

    # 2. Load DiseaseAndSymptoms.csv
    das_path = 'Dataset/DiseaseAndSymptoms.csv'
    df_das = pd.DataFrame()
    if os.path.exists(das_path):
        df_das_raw = pd.read_csv(das_path)
        df_das_raw = df_das_raw.dropna(subset=['Disease'])
        
        # Combine Symptom_1 to Symptom_17 into a single comma-separated string
        symptom_cols = [col for col in df_das_raw.columns if col.startswith('Symptom_')]
        def join_symptoms(row):
            # Extract valid symptoms and strip whitespaces
            symps = [str(x).strip() for x in row[symptom_cols] if pd.notna(x)]
            return ','.join(symps)
            
        df_das['Disease'] = df_das_raw['Disease'].str.strip().str.title()
        df_das['Symptoms'] = df_das_raw.apply(join_symptoms, axis=1)
        
        # Add missing demographic columns to df_das (impute later)
        df_das['Age'] = np.nan
        df_das['Gender'] = np.nan
        print(f"Loaded {len(df_das)} records from {das_path}")

    # 3. Normalize Disease names in Healthcare
    df_hc['Disease'] = df_hc['Disease'].str.strip().str.title()

    # 4. Merge the datasets
    df = pd.concat([df_hc, df_das], ignore_index=True)
    print(f"Total merged records: {len(df)}")

    # 5. Process Demographics
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age)
    
    gender_map = {'Male': 0, 'Female': 1, 'Other': 2}
    df['Gender_Code'] = df['Gender'].map(gender_map).fillna(2) # Map unknown/NaN to 'Other'

    # 6. Process Symptoms using MultiLabelBinarizer
    print("Processing symptoms...")
    # Clean up strings before splitting
    symptoms_series = df['Symptoms'].dropna().apply(lambda x: [s.strip().replace('_', ' ') for s in x.split(',') if s.strip()])

    print("Building feature matrix (this might take a moment)...")
    mlb = MultiLabelBinarizer()
    X_encoded = mlb.fit_transform(symptoms_series)
    unique_symptoms = list(mlb.classes_)
    print(f"Total unique symptoms found: {len(unique_symptoms)}")

    X_symptoms = pd.DataFrame(X_encoded, columns=unique_symptoms, index=symptoms_series.index)
    X_symptoms = X_symptoms.reindex(df.index, fill_value=0)

    # 7. Combine Demographics with Symptoms
    X = pd.concat([df[['Age', 'Gender_Code']], X_symptoms], axis=1)
    y = df['Disease']
    
    print(f"Total features used for training: {X.shape[1]}")
    
    # 8. Train the model (Optimized for low RAM usage < 512MiB)
    print("Training Lightweight Random Forest Classifier...")
    rf_clf = RandomForestClassifier(n_estimators=20, max_depth=25, random_state=42)
    rf_clf.fit(X, y)
    print(f"Model Training Complete. Accuracy on training set: {rf_clf.score(X, y) * 100:.2f}%")
    
    # 9. Save Models (with compression to stay under GitHub's 100MB limit)
    joblib.dump(rf_clf, 'model.pkl', compress=3)
    # Save all columns (which includes 'Age', 'Gender_Code', and symptoms)
    joblib.dump(list(X.columns), 'features.pkl')
    print(f"Model and features saved successfully. model.pkl size: {os.path.getsize('model.pkl') / 1024 / 1024:.2f} MB")
    
    # 10. Generate Precautions JSON mapping
    precautions_path = 'Dataset/Disease precaution.csv'
    precautions_data = {}
    if os.path.exists(precautions_path):
        df_prec = pd.read_csv(precautions_path)
        for index, row in df_prec.iterrows():
            if pd.notna(row['Disease']):
                disease_name = str(row['Disease']).strip().title()
                # Gather precuatios 1 to 4
                precs = [str(row[f'Precaution_{i}']).strip().title() for i in range(1, 5) if pd.notna(row.get(f'Precaution_{i}'))]
                precautions_data[disease_name] = precs
        
        with open('precautions.json', 'w') as f:
            json.dump(precautions_data, f)
        print("Generated precautions.json lookup.")

    # 11. Prepare analytics data
    print("Generating analytics data...")
    disease_counts = df['Disease'].value_counts().head(10).to_dict()
    symptom_frequencies = X_symptoms.sum().sort_values(ascending=False).head(10).to_dict()
    
    analytics_data = {
        'disease_distribution': {
            'labels': list(disease_counts.keys()),
            'values': list(disease_counts.values())
        },
        'top_symptoms': {
            'labels': list(symptom_frequencies.keys()),
            'values': list(symptom_frequencies.values())
        }
    }
    with open('analytics_data.json', 'w') as f:
        json.dump(analytics_data, f)
    print("Analytics data saved to analytics_data.json.")
    
    print("Process finished successfully!")
