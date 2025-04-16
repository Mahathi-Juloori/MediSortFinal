# triage_model.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import re

# Define column types
categorical_cols = ["Primary Symptom", "Additional Symptoms", "Pain Location", "Allergies"]
numerical_cols = ["Age", "Duration", "Severity"]
target_col = "Triage Category"

# Load data
print("Loading dataset...")
df = pd.read_csv("synthetic_triage_data.csv")

# Data cleaning and preprocessing
print("Cleaning data...")

# Process Age: ensure numeric
df["Age"] = pd.to_numeric(df["Age"], errors='coerce')
df["Age"].fillna(df["Age"].median(), inplace=True)

# Process Duration: handle text inputs like "2 days", "1 week"
def extract_duration(duration_str):
    # Convert to string in case it's already numeric
    duration_str = str(duration_str).lower()
    
    # Try to extract numeric part
    number_match = re.search(r'(\d+(\.\d+)?)', duration_str)
    if not number_match:
        return None
    
    number = float(number_match.group(1))
    
    # Adjust based on time unit
    if 'week' in duration_str:
        return number * 7  # Convert weeks to days
    elif 'month' in duration_str:
        return number * 30  # Approximate month as 30 days
    elif 'hour' in duration_str:
        return number / 24  # Convert hours to days
    else:  # Default to days
        return number

# Apply duration extraction
df["Duration"] = df["Duration"].apply(extract_duration)
df["Duration"].fillna(df["Duration"].median(), inplace=True)

# Process Severity: convert text values to numeric scale
def convert_severity(severity):
    severity_str = str(severity).lower()
    
    # If already numeric, return as float
    if severity_str.isdigit() or (severity_str.replace('.', '', 1).isdigit() and severity_str.count('.') < 2):
        return float(severity_str)
    
    # Map text values to numeric scale (1-10)
    if 'mild' in severity_str:
        return 3.0
    elif 'moderate' in severity_str:
        return 6.0
    elif 'severe' in severity_str:
        return 9.0
    else:
        return 5.0  # Default value for unknown entries

# Apply severity conversion
df["Severity"] = df["Severity"].apply(convert_severity)

# Quick data exploration
print(f"Dataset shape: {df.shape}")
print("\nTarget distribution:")
print(df[target_col].value_counts())

# Preprocess data
print("\nPreprocessing data...")
# Separate features and target
X = df.drop(target_col, axis=1)
y = df[target_col]

# Handle categorical features
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_cats = encoder.fit_transform(X[categorical_cols])
encoded_df = pd.DataFrame(
    encoded_cats, 
    columns=encoder.get_feature_names_out(categorical_cols)
)

# Process features
X_processed = X.drop(categorical_cols, axis=1)
X_processed = pd.concat([X_processed, encoded_df], axis=1)

# Scale numerical features
scaler = StandardScaler()
X_processed[numerical_cols] = scaler.fit_transform(X_processed[numerical_cols])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train model
print("\nTraining Random Forest model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot confusion matrix
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
           xticklabels=model.classes_,
           yticklabels=model.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

# Feature importance
if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 8))
    plt.title('Feature Importances')
    plt.bar(range(X_processed.shape[1]), importances[indices], align='center')
    plt.xticks(range(X_processed.shape[1]), [X_processed.columns[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.show()

# Save model and preprocessing components
print("\nSaving model...")
joblib.dump(model, 'triage_model.pkl')
joblib.dump(encoder, 'encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\nModel training complete!")

# Function for making predictions with flexible input handling
def predict_triage_category(patient_data):
    """
    Make triage prediction for a new patient with flexible input handling
    
    patient_data: dict with keys matching the required input fields
      Age: number (e.g., 45)
      Duration: string or number (e.g., "2 days" or 2)
      Primary Symptom: string (e.g., "Chest Pain")
      Additional Symptoms: string or list (e.g., "Fever, Cough" or ["Fever", "Cough"])
      Severity: string or number (e.g., "Moderate" or 6)
      Pain Location: string (e.g., "Chest")
      Allergies: string (e.g., "Penicillin" or "None")
    """
    # Load saved components
    model = joblib.load('triage_model.pkl')
    encoder = joblib.load('encoder.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Process the incoming data
    processed_data = patient_data.copy()
    
    # Handle Duration: convert text to numeric if needed
    if isinstance(processed_data["Duration"], str):
        processed_data["Duration"] = extract_duration(processed_data["Duration"])
    
    # Handle Severity: convert text to numeric scale if needed
    if not isinstance(processed_data["Severity"], (int, float)):
        processed_data["Severity"] = convert_severity(processed_data["Severity"])
    
    # Handle Additional Symptoms: convert list to comma-separated string if needed
    if isinstance(processed_data["Additional Symptoms"], list):
        processed_data["Additional Symptoms"] = ", ".join(processed_data["Additional Symptoms"])
    
    # Create DataFrame from patient data
    patient_df = pd.DataFrame([processed_data])
    
    # Process categorical features
    cat_features = encoder.transform(patient_df[categorical_cols])
    cat_df = pd.DataFrame(
        cat_features, 
        columns=encoder.get_feature_names_out(categorical_cols)
    )
    
    # Scale numerical features
    patient_df[numerical_cols] = scaler.transform(patient_df[numerical_cols])
    
    # Combine features
    patient_df = patient_df.drop(categorical_cols, axis=1)
    patient_df = pd.concat([patient_df, cat_df], axis=1)
    
    # Make prediction
    prediction = model.predict(patient_df)[0]
    probabilities = model.predict_proba(patient_df)[0]
    confidence = max(probabilities)
    
    return {
        "triage_category": prediction,
        "confidence": confidence,
        "probabilities": dict(zip(model.classes_, probabilities))
    }

def get_user_input():
    print("\n=== Medical Triage System ===")
    patient = {}
    
    patient["Age"] = int(input("Patient age: "))
    patient["Duration"] = input("Duration of symptoms (e.g., '2 days', '1 week'): ")
    patient["Primary Symptom"] = input("Primary symptom: ")
    
    additional = input("Additional symptoms (comma separated): ")
    patient["Additional Symptoms"] = additional
    
    severity_input = input("Severity (Mild/Moderate/Severe or 1-10): ")
    patient["Severity"] = severity_input
    
    patient["Pain Location"] = input("Pain location: ")
    patient["Allergies"] = input("Allergies (or 'None'): ")
    
    return patient

# Add this at the end of your script to create an interactive mode
if __name__ == "__main__":
    print("\nModel trained successfully! Ready for predictions.")
    while True:
        choice = input("\nMake a prediction? (y/n): ")
        if choice.lower() != 'y':
            break
            
        patient_data = get_user_input()
        result = predict_triage_category(patient_data)
        
        print("\n=== Triage Result ===")
        print(f"Recommended triage: {result['triage_category']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print("\nProbabilities:")
        for category, prob in result['probabilities'].items():
            print(f"  {category}: {prob:.2f}")