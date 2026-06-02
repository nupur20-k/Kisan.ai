# 🌱 KisanAI – Smart Farming AI
## Complete Setup Guide

---

## 📁 FOLDER STRUCTURE

```
smart-farming-ai/
│
├── index.html              ← Frontend (open this in browser)
├── app.py                  ← Flask ML backend API
├── requirements.txt        ← Python packages
├── Crop_recommendation.csv ← Dataset (download from Kaggle)
├── crop_model.pkl          ← Auto-generated after first run
├── scaler.pkl              ← Auto-generated after first run
├── encoder.pkl             ← Auto-generated after first run
└── README.md
```

---

## ⚡ STEP-BY-STEP SETUP

### Step 1 — Install Python (if not already)
Download Python 3.10+ from https://python.org

### Step 2 — Open terminal in project folder
```bash
cd smart-farming-ai
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get the real dataset (recommended)
1. Go to: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
2. Download `Crop_recommendation.csv`
3. Place it in the same folder as `app.py`

> If you skip this, the app auto-generates synthetic data and still works!

### Step 5 — Start the ML backend
```bash
python app.py
```
You'll see:
```
✅ Model trained! Accuracy: 99.2%
🚀 KisanAI backend running at http://localhost:5000
```

### Step 6 — Connect frontend to backend
Open `index.html`, find this line near the bottom of `<script>`:

```js
// To use real ML backend, replace submitPrediction() with this:
const API_URL = 'http://localhost:5000/predict';
```

In `submitPrediction()`, replace the `setTimeout(...)` block with:
```js
fetch(API_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    N: vals.n, P: vals.p, K: vals.k,
    temperature: vals.temp, humidity: vals.hum,
    ph: vals.ph, rainfall: vals.rain
  })
})
.then(r => r.json())
.then(data => {
  // use data.top_crops, data.tips, data.rotation
  renderResults(data);
});
```

### Step 7 — Open the app
Simply double-click `index.html` or open it in Chrome.

---

## 🧪 TEST THE API

Open browser or Postman:
```
GET  http://localhost:5000/health
POST http://localhost:5000/predict
Body: {"N":80,"P":40,"K":40,"temperature":26,"humidity":80,"ph":6.5,"rainfall":200}
```

---

## 🔬 ML MODEL DETAILS

| Item | Value |
|------|-------|
| Algorithm | Random Forest Classifier |
| Features | N, P, K, Temperature, Humidity, pH, Rainfall |
| Classes | 22 crop types |
| Accuracy | ~99% on Kaggle dataset |
| Training time | < 10 seconds |

---

## 🚀 HACKATHON UPGRADE IDEAS

1. **Live weather API** — use OpenWeatherMap free API to auto-fill temperature/humidity/rainfall by GPS location
2. **Disease detection** — add image upload + TensorFlow.js model to detect crop diseases from leaf photos
3. **Offline PWA** — add service worker to make the app work without internet (great for rural areas)
4. **Government scheme alerts** — scrape PM-Kisan and other scheme data to show relevant schemes
5. **Market price API** — connect to Agmarknet API for real mandi prices

---

## 💡 QUICK NOTES

- The app works **fully offline** without the Python backend (uses in-browser JS prediction)
- Adding the Python backend gives **real ML model accuracy (~99%)**
- Voice input works in **Chrome only** (Web Speech API)
- Multilingual support: **English, Hindi, Marathi**
