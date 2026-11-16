# SafeHer – Nationwide Women Safety Platform for India

SafeHer is a comprehensive, nationwide women safety analytics and risk mapping platform for India combining Data Science, Supervised Machine Learning, Geospatial Visualization, and Emergency Preparedness.

---

## Problem Statement

Women's safety is a foundational priority across India. While incident reports, emergency helplines, and support facilities exist across states and union territories, they are rarely unified into a transparent, accessible, and proactive situational platform. SafeHer addresses this challenge by providing:

- Comprehensive coverage across all 28 Indian States and 8 Union Territories
- Dynamic, searchable state, district, city, and locality hierarchy
- Geospatial mapping with incident clustering, kernel density heatmaps, and verified emergency facilities
- Supervised machine learning classifiers estimating relative situational risk
- Direct pan-India emergency response dialing (112, 181, 1091, 14490, 1930) and state-specific safety directories
- Session-based incident reporting and custom CSV dataset upload capabilities

> **Important Notice:** SafeHer is an analytical, educational, and situational awareness platform. Default records are synthetic demonstration data clearly marked as DEMO DATA. The platform does not predict individual criminal incidents or guarantee personal safety. In any acute physical emergency anywhere in India, call **112** immediately.

---

## Objectives

1. Nationwide Geographical Coverage: Support all 28 States and 8 Union Territories of India with authentic administrative hierarchy and valid centroid coordinates.
2. Geospatial Intelligence: Plot reported incident clusters, density heatmaps, and support infrastructure (police stations, hospitals, women help centres).
3. Machine Learning Risk Pipeline: Train, cross-validate, and evaluate multi-model classifiers (Logistic Regression, Decision Tree, Random Forest) with feature importance and confusion matrices.
4. Emergency Crisis Response: Provide instantaneous access to national and state-level emergency helplines, direct telephone dialing actions, and local trusted contacts with WhatsApp alerts.
5. Professional Design System: Modern light pastel lavender and blush-pink aesthetic with clean SVG vector iconography and zero decorative emojis.

---

## Key Modules

| Module | Route | Capabilities |
|---|---|---|
| **Home Dashboard** | `app.py` | Platform overview KPIs, emergency call action bar, interactive location explorer, incident reporting form, and module navigation cards |
| **Safety Map** | `pages/1_Safety_Map.py` | Interactive Folium map with clustering, heatmaps, support facilities, location search, and current location simulation |
| **Incident Analytics** | `pages/2_Incident_Analytics.py` | Multi-dimensional Plotly charts, category distributions, state comparisons, hour x day heatmaps, and CSV upload |
| **Risk Insights** | `pages/3_Risk_Insights.py` | Supervised ML pipeline (LR, DT, RF), 5-fold cross-validation, feature importance, confusion matrix, and scenario risk estimator |
| **Area Insights** | `pages/4_Area_Insights.py` | Multi-locality comparative metrics, data completeness indices, temporal distributions, and summary CSV export |
| **Emergency Support** | `pages/5_Emergency_Support.py` | National and state-specific helplines, SOS actions, trusted contact manager with WhatsApp alerts, and safety checklist |

---

## Technology Stack

- **Application Framework:** Streamlit
- **Runtime:** Python 3.12
- **Data Engineering:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (LogisticRegression, DecisionTreeClassifier, RandomForestClassifier)
- **Interactive Geospatial:** Folium, Streamlit-Folium
- **Visualization:** Plotly Express, Plotly Graph Objects
- **Model Serialization:** Joblib
- **Aesthetic Styling:** Custom CSS design system (pastel lavender `#B9A7E8` and blush pink `#FCECF3`)

---

## Project Structure

```
Women Safety/
├── app.py                          # Home Dashboard (entry point)
├── requirements.txt                # Python package dependencies
├── README.md                       # Platform documentation
├── .gitignore                      # Version control exclusions
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
│
├── assets/
│   └── safeher_icon.png            # Application logo and browser favicon
│
├── pages/                          # Multi-page application modules
│   ├── 1_Safety_Map.py             # Interactive nationwide safety map
│   ├── 2_Incident_Analytics.py     # Statistical charts and CSV upload
│   ├── 3_Risk_Insights.py          # Machine learning risk pipeline
│   ├── 4_Area_Insights.py          # Locality comparison and metrics
│   └── 5_Emergency_Support.py      # Emergency contacts, SOS & planning
│
├── src/                            # Reusable platform modules
│   ├── __init__.py
│   ├── geo_data.py                 # 28 States + 8 UTs administrative data
│   ├── data_generation.py          # Nationwide synthetic data generator
│   ├── data_processing.py          # Cleaning, filtering & incident recording
│   ├── analytics.py                # Plotly chart generation
│   ├── model_training.py           # Scikit-learn training & prediction
│   ├── mapping.py                  # Folium map builder
│   └── ui_components.py            # Global CSS and SVG vector icons
│
├── data/                           # Active datasets (clearly tagged)
│   ├── incidents.csv               # 2,500 nationwide synthetic incident records
│   └── support_locations.csv       # 342 police stations, hospitals, help centres
│
└── models/                         # Serialized machine learning models
    ├── safeher_risk_model.joblib   # Best classifier (Random Forest)
    └── label_encoders.joblib       # Categorical feature encoders
```

---

## Nationwide Coverage Details

SafeHer includes coverage across all 36 administrative entities of India:

- **28 States:** Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal.
- **8 Union Territories:** Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry.

---

## Machine Learning Pipeline

- **Target Variable:** `risk_label` (Binary: 0 = Lower Relative Risk, 1 = Higher Relative Risk).
- **Features Evaluated:** Hour of Day, Severity Level, Ambient Lighting, Transport Mode, Incident Category, Day of Week.
- **Validation:** Stratified 80/20 train/test hold-out split with 5-fold cross-validation.
- **Artifacts:** Best performing model (Random Forest) and feature encoders automatically saved to `models/`.

---

## How to Set Up and Run SafeHer

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your system
- A terminal (Terminal on macOS/Linux, PowerShell or Command Prompt on Windows)

---

### Step 1: Navigate to the Project Directory
Open your terminal and navigate to the project directory:

```bash
cd "Women Safety"
```

---

### Step 2: Create and Activate a Python Virtual Environment

#### On macOS / Linux:
```bash
# 1. Create a virtual environment named .venv
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate
```

#### On Windows (PowerShell):
```powershell
# 1. Create a virtual environment named .venv
python -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```
*(If you see an execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, or use Command Prompt: `.\.venv\Scripts\activate.bat`)*

---

### Step 3: Install Required Dependencies
With the virtual environment activated, install all required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Run the Automated Verification Suite (Optional but Recommended)
Verify that all administrative geo-data, datasets, ML models, and mapping engines are operating correctly:

```bash
python test_suite.py
```
You should see:
```text
=== 1. Testing geo_data ===
...
=== 7. Testing user incident reporting ===
ALL BACKEND MODULES AND VERIFICATIONS PASSED SUCCESSFULLY!
```

---

### Step 5: Start the SafeHer Web Application
Run the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will launch the local development server:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser to access the SafeHer platform.

---

### Troubleshooting
- **Port 8501 in use:** Run on a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Streamlit command not found:** Ensure your virtual environment is active, or use:
  ```bash
  python -m streamlit run app.py
  ```
- **macOS Xcode tools message:** If `python3` asks for Xcode developer tools on macOS, install them with `xcode-select --install` or use Python installed via [Homebrew](https://brew.sh) (`brew install python`) or the official [Python.org installer](https://www.python.org/downloads/).
