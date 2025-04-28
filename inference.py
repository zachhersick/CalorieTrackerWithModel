import joblib, pandas as pd
from tensorflow.keras.models import load_model

# Load your trained artifacts (you must save them after training)
model = load_model('model.h5')
scaler = joblib.load('scaler.pkl')

# Replace this with the exact feature order from your training DataFrame
feature_cols = [
  # e.g. 'Age', 'Weight', 'Height', 'Gender_male', 'Physical_Activity_Level_2', …
]

def predict_calories(data: dict) -> float:
    """
    data should include all keys in feature_cols with numeric values.
    """
    df = pd.DataFrame([data], columns=feature_cols)
    X_scaled = scaler.transform(df)
    pred = model.predict(X_scaled)
    return float(pred[0][0])
