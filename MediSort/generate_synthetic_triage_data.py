import random
import pandas as pd

# Extended symptom lists
primary_symptoms = [
    "Chest pain", "Fever", "Headache", "Abdominal pain", "Shortness of breath",
    "Cough", "Dizziness", "Nausea", "Back pain", "Fatigue",
    "Sore throat", "Vomiting", "Joint pain", "Blurred vision",
    "Diarrhea", "Palpitations", "Swelling", "Loss of consciousness",
    "Skin rash", "Itching", "Ear pain", "Runny nose", "Constipation",
    "Frequent urination", "Burning while urinating", "Tingling sensation",
    "Cold extremities", "Bruising", "Night sweats", "Weight loss",
    "Mood swings", "Muscle weakness"
]

additional_symptoms = [
    "Cough", "Fever", "Nausea", "Sore throat", "Vomiting", "Diarrhea",
    "Body ache", "Loss of smell", "Sneezing", "Rash", "Sweating",
    "Chills", "Light sensitivity", "Swelling", "Joint stiffness", "Cramping",
    "Burning sensation", "Anxiety", "Depression", "Loss of balance",
    "Frequent headaches", "Heartburn", "Tinnitus", "Sleep disturbances",
    "Tremors", "Dry mouth", "Hair loss"
]

pain_locations = [
    "Chest", "Lower abdomen", "Upper abdomen", "Back", "Head", "Legs", "Arms", "Neck"
]

severities = ["Mild", "Moderate", "Severe"]

allergy_options = ["None", "Penicillin", "Peanuts", "Dust", "Latex", "Pollen"]

triage_categories = ["Home Care", "Urgent", "Emergency"]

# Rule-based triage label assignment
def assign_triage(severity, primary_symptom, duration_days):
    if severity == "Severe" or primary_symptom in ["Chest pain", "Shortness of breath", "Loss of consciousness"]:
        return "Emergency"
    elif severity == "Moderate" or int(duration_days) > 3:
        return "Urgent"
    else:
        return "Home Care"

# Synthetic data generator
def generate_dataset(num_records=1000):
    data = []

    for _ in range(num_records):
        age = random.randint(1, 90)
        duration_days = random.randint(1, 10)
        duration = f"{duration_days} days"
        primary = random.choice(primary_symptoms)
        additional = random.sample(additional_symptoms, random.randint(0, 4))
        severity = random.choice(severities)
        location = random.choice(pain_locations)
        allergies = random.choice(allergy_options)
        triage = assign_triage(severity, primary, duration_days)

        data.append({
            "Age": age,
            "Duration": duration,
            "Primary Symptom": primary,
            "Additional Symptoms": ", ".join(additional),
            "Severity": severity,
            "Pain Location": location,
            "Allergies": allergies,
            "Triage Category": triage
        })

    df = pd.DataFrame(data)
    return df

# Run and save to CSV
if __name__ == "__main__":
    df = generate_dataset(1000)
    df.to_csv("synthetic_triage_data.csv", index=False)
    print("✅ synthetic_triage_data.csv generated successfully!")
