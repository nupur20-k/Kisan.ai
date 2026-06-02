# ============================================================
#  KisanAI – ML Backend
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os, warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# ── Profit table ──────────────────────────────────────────
PROFIT_DATA = {
    'rice': {'cost': 18000, 'sell': 40000, 'rotation': ['Legumes', 'Wheat']},
    'wheat': {'cost': 12000, 'sell': 30000, 'rotation': ['Mustard', 'Gram']},
    'maize': {'cost': 10000, 'sell': 25000, 'rotation': ['Soybean', 'Wheat']},
    'chickpea': {'cost': 8000, 'sell': 22000, 'rotation': ['Wheat', 'Rice']},
    'lentil': {'cost': 7000, 'sell': 18000, 'rotation': ['Wheat', 'Mustard']},
    'cotton': {'cost': 25000, 'sell': 60000, 'rotation': ['Wheat', 'Gram']},
    'sugarcane': {'cost': 30000, 'sell': 75000, 'rotation': ['Legumes', 'Wheat']},
    'soybean': {'cost': 12000, 'sell': 28000, 'rotation': ['Maize', 'Wheat']},
    'mango': {'cost': 20000, 'sell': 55000, 'rotation': ['Cover crops']},
    'banana': {'cost': 22000, 'sell': 50000, 'rotation': ['Legumes']},
    'grapes': {'cost': 35000, 'sell': 90000, 'rotation': ['Cover crops']},
    'orange': {'cost': 18000, 'sell': 45000, 'rotation': ['Legumes']},
    'papaya': {'cost': 12000, 'sell': 30000, 'rotation': ['Legumes']},
    'pomegranate': {'cost': 20000, 'sell': 55000, 'rotation': ['Cover crops']},
    'watermelon': {'cost': 8000, 'sell': 22000, 'rotation': ['Maize', 'Wheat']},
    'muskmelon': {'cost': 7000, 'sell': 18000, 'rotation': ['Wheat']},
    'coconut': {'cost': 15000, 'sell': 40000, 'rotation': ['Banana']},
    'jute': {'cost': 8000, 'sell': 20000, 'rotation': ['Rice']},
    'coffee': {'cost': 25000, 'sell': 70000, 'rotation': ['Shade trees']},
    'pigeonpea': {'cost': 6000, 'sell': 16000, 'rotation': ['Wheat', 'Rice']},
    'mothbeans': {'cost': 5000, 'sell': 13000, 'rotation': ['Sorghum']},
    'mungbean': {'cost': 6000, 'sell': 15000, 'rotation': ['Wheat']},
}

FARMING_TIPS = {
    'rice': ['Maintain water', 'Transplant at 3-4 weeks'],
    'wheat': ['Sow Oct-Nov', 'Irrigate properly'],
    'cotton': ['Use drip irrigation'],
    'maize': ['Plant in ridges'],
    'sugarcane': ['Avoid waterlogging'],
}
DEFAULT_TIPS = ['Test soil', 'Use compost']

# ── MODEL ────────────────────────────────────────────
def train_model():
    model_path = 'crop_model.pkl'
    scaler_path = 'scaler.pkl'
    encoder_path = 'encoder.pkl'

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f: model = pickle.load(f)
        with open(scaler_path, 'rb') as f: scaler = pickle.load(f)
        with open(encoder_path, 'rb') as f: le = pickle.load(f)
        return model, scaler, le

    df = pd.read_csv('Crop_recommendation.csv')
    X = df[['N','P','K','temperature','humidity','ph','rainfall']].values
    y = df['label'].values

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_enc)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    with open(model_path, 'wb') as f: pickle.dump(model, f)
    with open(scaler_path, 'wb') as f: pickle.dump(scaler, f)
    with open(encoder_path, 'wb') as f: pickle.dump(le, f)

    return model, scaler, le

model, scaler, le = train_model()

# ── API ────────────────────────────────────────────────

# FIXED HERE
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    # ✅ FIXED HERE
    if request.method == 'GET':
        return "API is working ✅"

    try:
        data = request.get_json()

        # ✅ FIXED HERE
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        features = np.array([[ 
            float(data.get('N',50)),
            float(data.get('P',40)),
            float(data.get('K',40)),
            float(data.get('temperature',25)),
            float(data.get('humidity',65)),
            float(data.get('ph',6.5)),
            float(data.get('rainfall',100)),
        ]])

        features_scaled = scaler.transform(features)
        proba = model.predict_proba(features_scaled)[0]
        top3_idx = np.argsort(proba)[::-1][:3]

        results = []
        for idx in top3_idx:
            crop_name = le.inverse_transform([idx])[0]
            score = round(float(proba[idx])*100,1)

            pdata = PROFIT_DATA.get(crop_name.lower(), {'cost':10000,'sell':25000,'rotation':['Wheat']})

            results.append({
                'crop': crop_name,
                'match': score,
                'profit': pdata['sell'] - pdata['cost']
            })

        return jsonify({'top_crops': results})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    app.run(debug=True)