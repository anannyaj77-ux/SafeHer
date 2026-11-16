"""
app.py – SafeHer: Nationwide Women Safety Platform
Home Dashboard
"""

import sys
import os
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd

from data_processing import (
    get_active_incidents, load_support_locations, get_summary_stats,
    record_user_incident,
)
from data_generation import save_datasets
from geo_data import (
    STATES_AND_UTS, get_all_states, get_cities_for_state,
    get_areas_for_city, search_locations, get_state_info,
)
from ui_components import get_global_css, get_icon

# ── Page config ───────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "SafeHer – Nationwide Women Safety Platform",
    page_icon  = icon_path,
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Ensure data exists ─────────────────────────────────────────────────────────
save_datasets(ROOT / "data")

# ── Load data ─────────────────────────────────────────────────────────────────
df, source = get_active_incidents()
df_support = load_support_locations()
stats      = get_summary_stats(df)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:12px 0 16px 0;">
      <div style="display:inline-flex;padding:12px;background:#FFFFFF;border-radius:18px;border:1px solid #E8DDF2;box-shadow:0 2px 10px rgba(185,167,232,0.15);margin-bottom:8px;">
        {get_icon("shield")}
      </div>
      <div style="font-size:1.55rem;font-weight:700;color:#392E4D;letter-spacing:-0.01em;">SafeHer</div>
      <div style="font-size:0.8rem;color:#7B5EA7;font-weight:600;">Nationwide Women Safety Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Navigation**")
    st.page_link("app.py", label="Home Dashboard")
    st.page_link("pages/1_Safety_Map.py", label="Safety Map")
    st.page_link("pages/2_Incident_Analytics.py", label="Incident Analytics")
    st.page_link("pages/3_Risk_Insights.py", label="Risk Insights")
    st.page_link("pages/4_Area_Insights.py", label="Area Insights")
    st.page_link("pages/5_Emergency_Support.py", label="Emergency Support")

    st.markdown("---")
    st.markdown("**Emergency Helpline**")
    st.markdown("""
    <div style="background:#FFF0F5;border:1px solid #F2BFD1;border-radius:12px;padding:12px;text-align:center;">
      <div style="font-size:0.78rem;color:#8C395B;font-weight:600;text-transform:uppercase;">Immediate Danger</div>
      <div style="font-size:1.6rem;font-weight:800;color:#C0392B;line-height:1.2;">112</div>
      <div style="font-size:0.75rem;color:#6B4E57;margin-top:2px;">Pan-India Emergency Service</div>
      <div style="margin-top:8px;">
        <a href="tel:112" style="display:inline-block;background:#C0392B;color:white;padding:5px 14px;border-radius:8px;font-size:0.8rem;text-decoration:none;font-weight:600;">Call 112</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Data Integrity**")
    if source == "demo":
        st.info("Demonstration dataset active across all 28 States and 8 UTs. User CSV upload available in Incident Analytics.")
    else:
        st.success("Custom user dataset active.")

    st.markdown(
        "<div style='text-align:center;color:#81768E;font-size:0.76rem;margin-top:16px;'>SafeHer Platform · Nationwide Coverage · India</div>",
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
#  HERO SECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:12px;">
    {get_icon("shield")} Nationwide Women Safety Initiative · India
  </div>
  <h1 class="page-header-title">Your Safety. Your Awareness. Nationwide.</h1>
  <p class="page-header-desc">
    SafeHer provides unified safety intelligence, interactive geospatial risk mapping,
    and instantaneous access to verified emergency infrastructure across all 28 Indian States
    and 8 Union Territories.
  </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIORITY 1: EMERGENCY SUPPORT SECTION (PROMINENT ACCESS)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="emergency-banner-bar">
  <div class="emergency-banner-title">
    {get_icon("alert")}
    <span>Immediate Emergency Assistance</span>
  </div>
  <div class="emergency-banner-sub">
    If you or someone around you is in immediate distress or danger, connect directly with official national emergency responders.
  </div>
</div>
""", unsafe_allow_html=True)

sos_col1, sos_col2, sos_col3, sos_col4, sos_col5 = st.columns(5)
helpline_actions = [
    (sos_col1, "112", "National Emergency (ERSS)", "tel:112", "#C0392B"),
    (sos_col2, "181", "Women Helpline", "tel:181", "#7B5EA7"),
    (sos_col3, "1091", "Women in Distress", "tel:1091", "#7B5EA7"),
    (sos_col4, "14490", "NCW Women Support", "tel:14490", "#7B5EA7"),
    (sos_col5, "1930", "Cyber Harassment Helpline", "tel:1930", "#2980B9"),
]
for col, num, title, link, border_col in helpline_actions:
    with col:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-top:3px solid {border_col};border-radius:12px;padding:14px;text-align:center;box-shadow:0 2px 8px rgba(185,167,232,0.12);margin-bottom:10px;">
          <div style="font-size:1.6rem;font-weight:800;color:{border_col};">{num}</div>
          <div style="font-size:0.78rem;font-weight:600;color:#392E4D;margin:3px 0 8px 0;min-height:32px;">{title}</div>
          <a href="{link}" style="display:block;background:#F5F0FF;border:1px solid #B9A7E8;color:#392E4D;padding:6px;border-radius:8px;font-size:0.8rem;font-weight:600;text-decoration:none;">Call {num}</a>
        </div>
        """, unsafe_allow_html=True)

# State-Specific Helpline Quick Finder
with st.expander("Find Emergency Numbers for Your State or Union Territory", expanded=False):
    sel_st = st.selectbox("Select State or Union Territory", get_all_states(), index=get_all_states().index("Delhi") if "Delhi" in get_all_states() else 0)
    st_info = get_state_info(sel_st)
    if st_info:
        c_st1, c_st2, c_st3 = st.columns(3)
        with c_st1:
            st.markdown(f"**Entity Type:** {st_info['type']}")
            st.markdown(f"**Administrative Capital:** {st_info['capital']}")
        with c_st2:
            st.markdown(f"**Dedicated State Helpline:** `{st_info.get('helpline', '112')}`")
            st.markdown(f"**Coverage:** All districts & major transit hubs")
        with c_st3:
            st.markdown(f"**National Emergency Response:** `112` (24x7 toll-free)")
            st.page_link("pages/1_Safety_Map.py", label=f"View {sel_st} on Safety Map")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIORITY 2 & 3: LOCATION EXPLORER & INCIDENT REPORTING
# ═══════════════════════════════════════════════════════════════════════════════
col_loc, col_rep = st.columns([1, 1], gap="medium")

with col_loc:
    st.markdown(f'<div class="section-heading-custom">{get_icon("map")} Nationwide Location Explorer</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem;color:#6D6180;'>Select any region across India to view available safety reports and emergency infrastructure.</p>", unsafe_allow_html=True)

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        chosen_state = st.selectbox("State / Union Territory", get_all_states(), key="home_state_select")
    with c_s2:
        avail_cities = get_cities_for_state(chosen_state)
        chosen_city = st.selectbox("District / City", avail_cities, key="home_city_select")

    # Localities
    avail_areas = get_areas_for_city(chosen_state, chosen_city)
    chosen_area = st.selectbox("Locality / Sector", ["All Areas"] + avail_areas, key="home_area_select")

    # Filtered preview stats
    if not df.empty and "state" in df.columns and "city" in df.columns:
        loc_filtered = df[(df["state"] == chosen_state) & (df["city"] == chosen_city)]
        if chosen_area != "All Areas" and "area" in loc_filtered.columns:
            loc_filtered = loc_filtered[loc_filtered["area"] == chosen_area]
    else:
        loc_filtered = pd.DataFrame()

    if not df_support.empty and "state" in df_support.columns and "city" in df_support.columns:
        sup_filtered = df_support[(df_support["state"] == chosen_state) & (df_support["city"] == chosen_city)]
    else:
        sup_filtered = pd.DataFrame()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Reported Incidents", f"{len(loc_filtered)}")
    with m2:
        st.metric("Support Units", f"{len(sup_filtered)}")
    with m3:
        high_sev = int((loc_filtered["severity"] == 3).sum()) if not loc_filtered.empty else 0
        st.metric("High Severity", f"{high_sev}")

    st.page_link("pages/1_Safety_Map.py", label="Open in Interactive Safety Map", icon=":material/arrow_forward:")

with col_rep:
    st.markdown(f'<div class="section-heading-custom">{get_icon("shield")} Report an Incident</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem;color:#6D6180;'>Submit an incident report for your locality. Reports immediately reflect in your active session analytics.</p>", unsafe_allow_html=True)

    with st.expander("Submit Incident Report", expanded=True):
        with st.form("home_incident_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                rep_state = st.selectbox("State / UT", get_all_states(), key="rep_state")
            with fc2:
                rep_cities = get_cities_for_state(rep_state)
                rep_city = st.selectbox("City / District", rep_cities, key="rep_city")

            fc3, fc4 = st.columns(2)
            with fc3:
                rep_areas = get_areas_for_city(rep_state, rep_city)
                rep_area = st.selectbox("Locality / Area", rep_areas if rep_areas else ["General Area"], key="rep_area")
            with fc4:
                rep_cat = st.selectbox("Category", [
                    "Verbal Harassment", "Physical Harassment", "Stalking",
                    "Eve Teasing", "Theft / Snatching", "Unsafe Environment",
                    "Online Harassment", "Domestic Dispute",
                ])

            fc5, fc6, fc7 = st.columns(3)
            with fc5:
                rep_sev = st.select_slider("Severity Level", options=[1, 2, 3], value=2,
                                           format_func=lambda x: {1: "1 - Low", 2: "2 - Medium", 3: "3 - High"}[x])
            with fc6:
                rep_lighting = st.selectbox("Lighting", ["Well-lit", "Adequate", "Poorly-lit", "Very Dark"])
            with fc7:
                rep_transport = st.selectbox("Transport", ["Walking", "Bus", "Metro", "Auto", "Cab", "Two-Wheeler", "Other"])

            rep_desc = st.text_input("Incident Summary (Optional)", placeholder="Brief contextual description")

            submitted = st.form_submit_button("Submit Report")
            if submitted:
                success, msg = record_user_incident({
                    "state": rep_state,
                    "city": rep_city,
                    "area": rep_area,
                    "category": rep_cat,
                    "severity": rep_sev,
                    "lighting": rep_lighting,
                    "transport_mode": rep_transport,
                    "description": rep_desc,
                })
                if success:
                    st.success(f"{msg} Your record is now visible on the Safety Map and Analytics.")
                    st.rerun()
                else:
                    st.error(msg)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  KPI CARDS: NATIONWIDE PLATFORM OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("analytics")} Nationwide Platform Overview</div>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpis = [
    (kpi1, str(stats["total"]), "Total Incidents", "analytics"),
    (kpi2, str(stats.get("states", 36)), "States & UTs Covered", "shield"),
    (kpi3, str(stats["cities"]), "Districts & Cities", "area"),
    (kpi4, str(len(df_support)), "Support Locations", "hospital"),
    (kpi5, str(stats["date_range"]), "Data Period", "calendar"),
]
for col, num, label, icon_name in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon">{get_icon(icon_name)}</div>
          <div class="kpi-number">{num}</div>
          <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIORITY 4 & 5: NAVIGATION CARDS TO ALL 5 MODULES
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("shield")} Explore SafeHer Modules</div>', unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5 = st.columns(5)
modules = [
    (nav1, "Emergency Support", "Verified national & state helplines, direct-dial crisis actions, personal trusted contacts, and safety planning checklist.", "pages/5_Emergency_Support.py", "phone"),
    (nav2, "Safety Map", "Geospatial mapping across India with incident clustering, density heatmaps, police stations, hospitals, and location filtering.", "pages/1_Safety_Map.py", "map"),
    (nav3, "Incident Analytics", "Analytical breakdowns by category, hour of day, day of week, time period, and CSV dataset upload.", "pages/2_Incident_Analytics.py", "analytics"),
    (nav4, "Risk Insights", "Machine learning classification models (Logistic Regression, Decision Tree, Random Forest) with feature importance.", "pages/3_Risk_Insights.py", "brain"),
    (nav5, "Area Insights", "Comparative safety analysis across Indian cities and neighbourhoods with completeness metrics and reporting caveats.", "pages/4_Area_Insights.py", "area"),
]

for col, title, desc, target_page, icon_name in modules:
    with col:
        st.markdown(f"""
        <div class="nav-card">
          <div class="nav-card-icon">{get_icon(icon_name)}</div>
          <div class="nav-card-title">{title}</div>
          <div class="nav-card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(target_page, label=f"Open {title}")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  HOW SAFHER WORKS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("info")} Architecture and Workflow</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
steps = [
    (s1, "1", "Data Integration", "Nationwide incident datasets covering all 28 states and 8 union territories, clearly labelled as demonstration or user-uploaded records."),
    (s2, "2", "Spatial & Statistical Analytics", "Interactive Folium geospatial layers, kernel density heatmaps, and multi-dimensional Plotly visualizations."),
    (s3, "3", "Machine Learning Pipeline", "Scikit-learn models evaluate relative risk indications based on temporal, environmental, and situational factors."),
    (s4, "4", "Emergency Action Support", "Direct connection to pan-India helplines (112, 181, 1091) and verified nearby emergency support infrastructure."),
]
for col, num, title, desc in steps:
    with col:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:14px;padding:20px;height:100%;box-shadow:0 2px 8px rgba(185,167,232,0.08);">
          <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#B9A7E8,#F2BFD1);color:#392E4D;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:10px;">{num}</div>
          <div style="font-weight:700;color:#392E4D;font-size:0.98rem;margin-bottom:6px;">{title}</div>
          <div style="font-size:0.84rem;color:#6D6180;line-height:1.55;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TRANSPARENT DISCLAIMER
# ═══════════════════════════════════════════════════════════════════════════════
if source == "demo":
    disclaimer_lead = "The active records are synthetic demonstration data created for nationwide architectural representation across India."
else:
    disclaimer_lead = "The active dataset is user-uploaded and has not been verified by law enforcement authorities."

st.markdown(f"""
<div class="clean-disclaimer">
  <div style="font-weight:700;color:#392E4D;margin-bottom:4px;">Platform Disclaimer and Data Transparency</div>
  SafeHer is an analytical, educational, and situational awareness platform. {disclaimer_lead}
  Risk ratings and indicators are relative and indicative; they do not predict individual criminal incidents or guarantee personal safety.
  Local reporting rates, public awareness, and data completeness influence all statistical patterns shown.
  In an immediate emergency anywhere in India, call <strong>112</strong> immediately.
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #E8DDF2;margin-top:24px;padding-top:16px;text-align:center;color:#81768E;font-size:0.8rem;">
  SafeHer · Nationwide Women Safety & Risk Mapping Platform · Built with Python, Streamlit, Scikit-learn & Folium
</div>
""", unsafe_allow_html=True)
