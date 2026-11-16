"""
pages/3_Risk_Insights.py – SafeHer: Risk Insights & ML Pipeline
Machine learning risk pipeline: model training, cross-validation, feature importance,
confusion matrix analysis, and scenario-based relative risk estimation.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd
import numpy as np

from data_processing import get_active_incidents
from model_training import (
    train_all_models, get_model_metrics_summary,
    predict_risk, load_saved_model,
)
import analytics as an
from geo_data import get_all_states, get_cities_for_state
from ui_components import get_global_css, get_icon

# ── Page config ────────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "Risk Insights – SafeHer",
    page_icon  = icon_path,
    layout     = "wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:10px;">
    {get_icon("brain")} Supervised Machine Learning Pipeline
  </div>
  <h1 class="page-header-title">Risk Insights & Machine Learning Pipeline</h1>
  <p class="page-header-desc">
    Train, validate, and evaluate predictive machine learning classifiers to estimate relative situational
    risk based on temporal, situational, and environmental indicators. All model outputs are indicative.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {get_icon('brain')} Model Training Controls", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Models are trained on the active dataset. Demonstration records reflect synthetic nationwide data; uploaded datasets require an explicit risk_label target.")

    retrain = st.button("Retrain Models on Active Data", help="Re-run stratified 80/20 train-test split and 5-fold cross validation.")
    st.markdown("---")
    st.markdown("**ML Architecture Overview**")
    st.markdown("""
    **Target Variable**: `risk_label`  
    - `0` = Lower Relative Risk  
    - `1` = Higher Relative Risk  

    **Feature Vector**:
    - Hour of Day (0–23)
    - Scenario Severity (1–3)
    - Ambient Lighting Condition
    - Primary Transport Mode
    - Incident Category
    - Day of Week

    **Evaluated Classifiers**:
    - Logistic Regression (with StandardScaler)
    - Decision Tree Classifier
    - Random Forest Classifier (100 estimators)
    """)

# ── Load active data ───────────────────────────────────────────────────────────
df, _source = get_active_incidents()

# ── Train or load cached results ──────────────────────────────────────────────
train_key = "ml_results"
data_signature = int(pd.util.hash_pandas_object(df, index=True).sum()) if not df.empty else 0

if retrain or train_key not in st.session_state or st.session_state.get("ml_data_signature") != data_signature:
    with st.spinner("Training baseline classifiers and running 5-fold cross-validation…"):
        results = train_all_models(df)
        st.session_state[train_key] = results
        st.session_state["ml_data_signature"] = data_signature
else:
    results = st.session_state[train_key]

if not results:
    if "risk_label" not in df.columns:
        st.info("The active dataset does not contain an explicit risk_label target column. Please upload a CSV with a binary 0/1 target to train custom models.")
    else:
        st.warning("Insufficient samples to train models. At least 100 rows with both classes (0 and 1) are required.")
    st.stop()

meta     = results["_meta"]
best_key = meta["best_model"]
best     = results[best_key]

# ── Best Model Banner ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #E8DDF2;border-left:4px solid #7B5EA7;border-radius:14px;padding:16px 24px;margin-bottom:20px;box-shadow:0 2px 10px rgba(185,167,232,0.10);display:flex;align-items:center;justify-content:space-between;">
  <div>
    <span class="status-pill">Selected Baseline Model</span>
    <span style="font-size:1.2rem;font-weight:700;color:#392E4D;margin-left:10px;">{best_key}</span>
    <span style="color:#81768E;font-size:0.86rem;margin-left:8px;">(Optimal hold-out F1 Score on test set)</span>
  </div>
  <div style="font-size:0.82rem;color:#7B5EA7;font-weight:600;">
    Train: {meta['train_size']:,} · Test: {meta['test_size']:,}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Key Metrics Cards ──────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
metrics_data = [
    (m1, f"{best['accuracy']*100:.1f}%",  "Accuracy", "check"),
    (m2, f"{best['precision']*100:.1f}%", "Precision", "shield"),
    (m3, f"{best['recall']*100:.1f}%",    "Recall", "locate"),
    (m4, f"{best['f1']*100:.1f}%",        "F1 Score", "brain"),
    (m5, f"{best['cv_f1']*100:.1f}%",     "CV F1 (5-Fold)", "analytics"),
]
for col, val, label, icon_name in metrics_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon">{get_icon(icon_name)}</div>
          <div class="kpi-number">{val}</div>
          <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Model Performance Comparison",
    "Confusion Matrix Analysis",
    "Feature Importance",
    "Classification Report",
    "Scenario Risk Estimator",
])

# ── TAB 1: Comparison ────────────────────────────────────────────────────────
with tab1:
    df_metrics = get_model_metrics_summary(results)
    st.dataframe(df_metrics, width="stretch", hide_index=True)

    comp_dict = {
        name: {
            "Accuracy":  res["accuracy"],
            "Precision": res["precision"],
            "Recall":    res["recall"],
            "F1 Score":  res["f1"],
            "CV F1":     res["cv_f1"],
        }
        for name, res in results.items() if name != "_meta"
    }
    st.plotly_chart(an.chart_model_comparison(comp_dict), use_container_width=True)

    disclaimer_text = (
        "Models trained on synthetic nationwide data. Metrics describe statistical characteristics of this generated dataset and demonstrate machine learning evaluation methodology."
        if _source == "demo" else
        "Models trained on user-uploaded dataset. Confirm training sample validity and labels before relying on predictions."
    )
    st.markdown(f"""
    <div class="clean-disclaimer">
      <strong>Model Evaluation Context:</strong> Stratified hold-out split (80% training / 20% validation) with 5-fold cross-validation.
      {disclaimer_text}
    </div>
    """, unsafe_allow_html=True)

# ── TAB 2: Confusion Matrix ───────────────────────────────────────────────────
with tab2:
    cm_model = st.selectbox("Inspect Classifier Confusion Matrix", [k for k in results.keys() if k != "_meta"], key="cm_sel")
    chosen = results[cm_model]
    cm = chosen["cm"]

    c_cm1, c_cm2 = st.columns([1.2, 1])
    with c_cm1:
        st.plotly_chart(an.chart_confusion_matrix(cm), use_container_width=True)
    with c_cm2:
        st.markdown("### Matrix Interpretation")
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
        st.markdown(f"""
        | Metric Category | Count | Operational Definition |
        |---|---|---|
        | **True Negative** | **{tn}** | Correctly identified lower-risk scenarios |
        | **False Positive** | **{fp}** | Lower-risk scenario flagged as higher risk |
        | **False Negative** | **{fn}** | Higher-risk scenario missed (Critical Safety Error) |
        | **True Positive** | **{tp}** | Correctly detected higher-risk situations |

        **Safety Consideration:** In safety and risk mapping, minimizing False Negatives is prioritized to ensure hazardous contexts are not mischaracterized as benign.
        """)

# ── TAB 3: Feature Importance ─────────────────────────────────────────────────
with tab3:
    fi_model = st.selectbox("Inspect Feature Weights", [k for k in results.keys() if k != "_meta"], key="fi_sel")
    fi_data  = results[fi_model]
    fi_vals  = fi_data["feature_importance"]
    fi_names = fi_data["feature_names"]

    label_map = {
        "hour":            "Hour of Day",
        "severity":        "Severity Level",
        "lighting_enc":    "Ambient Lighting",
        "transport_enc":   "Transport Mode",
        "category_enc":    "Incident Category",
        "day_of_week_enc": "Day of Week",
    }
    readable_names = [label_map.get(n, n) for n in fi_names]
    st.plotly_chart(an.chart_feature_importance(readable_names, fi_vals), use_container_width=True)

    st.markdown("""
    <div class="clean-disclaimer">
      <strong>Feature Importance Interpretation:</strong> Importance scores quantify each factor's relative contribution to classification splits within the model.
      Higher importance signifies stronger statistical correlation within the training dataset; it does not constitute direct causation.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 4: Classification Report ──────────────────────────────────────────────
with tab4:
    cr_model = st.selectbox("Inspect Classification Report", [k for k in results.keys() if k != "_meta"], key="cr_sel")
    rep = results[cr_model]["report"]
    rep_rows = []
    for cls_name, vals in rep.items():
        if isinstance(vals, dict):
            rep_rows.append({
                "Evaluation Class": "Class 0 (Lower Risk)" if cls_name == "0" else "Class 1 (Higher Risk)" if cls_name == "1" else cls_name.title(),
                "Precision": round(vals.get("precision", 0), 4),
                "Recall": round(vals.get("recall", 0), 4),
                "F1 Score": round(vals.get("f1-score", 0), 4),
                "Sample Support": int(vals.get("support", 0)),
            })
    st.dataframe(pd.DataFrame(rep_rows), width="stretch", hide_index=True)

# ── TAB 5: Scenario Risk Estimator ────────────────────────────────────────────
with tab5:
    st.markdown("### Estimate Relative Situational Risk")
    st.markdown("Enter environmental and temporal parameters to observe model predictions based on statistical relationships learned from the nationwide dataset.")

    p1, p2 = st.columns(2)
    with p1:
        p_state = st.selectbox("Context Region (State / UT)", get_all_states(), index=0, key="ml_pred_state")
        p_cities = get_cities_for_state(p_state)
        p_city = st.selectbox("City / District", p_cities, key="ml_pred_city")
        p_hour = st.slider("Hour of Day (0–23)", 0, 23, 21, help="24-hour military time format")
        p_sev  = st.selectbox("Incident Severity Reference", [1, 2, 3],
                              format_func=lambda x: {1: "1 - Low", 2: "2 - Medium", 3: "3 - High"}[x])
    with p2:
        p_lighting = st.selectbox("Ambient Lighting Condition", ["Well-lit", "Adequate", "Poorly-lit", "Very Dark"])
        p_transport = st.selectbox("Mode of Travel", ["Walking", "Bus", "Metro", "Auto", "Cab", "Train", "Two-Wheeler", "Other"])
        p_category  = st.selectbox("Incident Category", [
            "Verbal Harassment", "Physical Harassment", "Stalking",
            "Eve Teasing", "Theft / Snatching", "Unsafe Environment",
            "Online Harassment", "Domestic Dispute",
        ])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Calculate Relative Risk Estimation"):
        input_dict = {
            "hour":           p_hour,
            "severity":       p_sev,
            "lighting":       p_lighting,
            "transport_mode": p_transport,
            "category":       p_category,
        }
        pred = predict_risk(input_dict)

        if pred is None:
            st.error("Model prediction pipeline currently unavailable. Please retrain.")
        elif pred == 1:
            st.markdown(f"""
            <div style="background:#FFF0F5;border:1.5px solid #F2BFD1;border-radius:14px;padding:20px;text-align:center;box-shadow:0 3px 12px rgba(242,191,209,0.3);margin-top:12px;">
              <div style="color:#C0392B;font-weight:700;font-size:1.3rem;margin-bottom:6px;">Higher Relative Risk Indicated</div>
              <div style="color:#6B4E57;font-size:0.92rem;max-width:700px;margin:0 auto;line-height:1.6;">
                The trained model associates this parameter combination (late night hours, reduced ambient lighting, or vulnerable travel modes)
                with a heightened probability of severe incidents.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#F5F0FF;border:1.5px solid #B9A7E8;border-radius:14px;padding:20px;text-align:center;box-shadow:0 3px 12px rgba(185,167,232,0.2);margin-top:12px;">
              <div style="color:#4A2D75;font-weight:700;font-size:1.3rem;margin-bottom:6px;">Lower Relative Risk Indicated</div>
              <div style="color:#574A6A;font-size:0.92rem;max-width:700px;margin:0 auto;line-height:1.6;">
                The trained model associates this combination with reduced relative severity within the dataset.
                No setting is completely immune; always maintain personal situational awareness.
              </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="clean-disclaimer" style="margin-top:24px;">
  <strong>Machine Learning Notice:</strong> Model evaluations and risk estimators are algorithmic approximations derived from dataset patterns.
  They are not deterministic personal safety guarantees. For immediate physical safety, call <strong>112</strong> immediately.
</div>
""", unsafe_allow_html=True)
