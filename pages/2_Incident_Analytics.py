"""
pages/2_Incident_Analytics.py – SafeHer: Incident Analytics
Comprehensive nationwide analytics: category breakdowns, state-level analysis,
temporal trends, hourly distribution, and custom dataset management.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd
import io

from data_processing import (
    get_active_incidents, filter_incidents,
    validate_incident_columns, clean_incidents,
)
import analytics as an
from geo_data import get_all_states, get_cities_for_state
from ui_components import get_global_css, get_icon

# ── Page config ────────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "Incident Analytics – SafeHer",
    page_icon  = icon_path,
    layout     = "wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:10px;">
    {get_icon("analytics")} Statistical & Behavioral Insights
  </div>
  <h1 class="page-header-title">Incident Analytics</h1>
  <p class="page-header-desc">
    Explore analytical distributions, temporal dynamics, transport correlations, and nationwide
    safety patterns across Indian states and union territories.
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR: DATA MANAGEMENT & FILTERS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### Dataset Source")

    upload_version = st.session_state.get("safeher_upload_version", 0)
    upload = st.file_uploader(
        "Upload Custom CSV Dataset",
        type=["csv"],
        key=f"safeher_incident_upload_{upload_version}",
        help="Required columns: date, latitude, longitude, category, severity, city, area, hour, time_of_day. An explicit risk_label column is required for ML.",
    )

    if st.button("Reset to Nationwide Demo Dataset", help="Clear custom uploaded data and restore default nationwide records."):
        st.session_state.pop("safeher_uploaded_incidents", None)
        st.session_state["safeher_upload_version"] = upload_version + 1
        st.rerun()

    if upload:
        try:
            user_df = pd.read_csv(upload)
            ok, msg = validate_incident_columns(user_df)
            if not ok:
                st.error(f"File Validation Error: {msg}")
                df_source, source_label = get_active_incidents()
            else:
                df_source = clean_incidents(user_df)
                if df_source.empty:
                    st.error("No valid records remain after date and coordinate verification.")
                    df_source, source_label = get_active_incidents()
                else:
                    st.session_state["safeher_uploaded_incidents"] = df_source.copy()
                    source_label = "uploaded"
                    st.success(f"Loaded {len(df_source):,} records. Active across all pages.")
        except Exception as e:
            st.error(f"Read Error: {e}")
            df_source, source_label = get_active_incidents()
    else:
        df_source, source_label = get_active_incidents()

    st.markdown("---")
    st.markdown("### Filter Criteria")

    if df_source.empty:
        st.error("No usable records available. Please upload a valid CSV or reset.")
        st.stop()

    # Nationwide State Filter
    if "state" in df_source.columns:
        all_states = ["All States & UTs"] + sorted(df_source["state"].dropna().unique().tolist())
        sel_state = st.selectbox("State / Union Territory", all_states, index=0)
    else:
        sel_state = "All States & UTs"

    # City Filter
    if sel_state != "All States & UTs" and "state" in df_source.columns:
        sub_cities = sorted(df_source[df_source["state"] == sel_state]["city"].dropna().unique().tolist())
    else:
        sub_cities = sorted(df_source["city"].dropna().unique().tolist())

    sel_cities = st.multiselect("Districts / Cities", sub_cities, default=None)

    all_cats = sorted(df_source["category"].dropna().unique().tolist())
    sel_cats = st.multiselect("Incident Categories", all_cats, default=None)

    all_periods = ["Morning", "Afternoon", "Evening", "Night"]
    sel_periods = st.multiselect("Time of Day", all_periods, default=None)

    all_sev = [1, 2, 3]
    sel_sev = st.multiselect("Severity (1=Low, 3=High)", all_sev, default=None)

    if "date" in df_source.columns and not df_source["date"].dropna().empty:
        valid_dates = pd.to_datetime(df_source["date"].dropna())
        min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
    else:
        min_d, max_d = pd.Timestamp("2021-01-01").date(), pd.Timestamp.now().date()
    date_range = st.date_input("Date Period", (min_d, max_d), min_value=min_d, max_value=max_d)

    st.markdown("---")
    st.caption("Visualizations refresh dynamically as filters update.")

# ── Apply filters ──────────────────────────────────────────────────────────────
filter_states = [sel_state] if sel_state != "All States & UTs" else None
df = filter_incidents(
    df_source,
    states       = filter_states,
    cities       = sel_cities or None,
    categories   = sel_cats or None,
    time_periods = sel_periods or None,
    severity     = sel_sev or None,
    date_range   = (date_range[0], date_range[1]) if len(date_range) == 2 else None,
)

# Notification banner
if source_label == "demo":
    st.info("Demonstration nationwide dataset active. Upload custom CSV files via the sidebar to analyze your own data.")
else:
    st.success(f"Using user-uploaded dataset ({len(df):,} filtered of {len(df_source):,} total records).")

if df.empty:
    st.warning("No records found for the chosen filters. Try broadening the selection.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  METRICS OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{get_icon("analytics")}</div>
      <div class="kpi-number">{len(df):,}</div>
      <div class="kpi-label">Filtered Incidents</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    states_count = df["state"].nunique() if "state" in df.columns else 1
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{get_icon("shield")}</div>
      <div class="kpi-number">{states_count}</div>
      <div class="kpi-label">States / UTs</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    cities_count = df["city"].nunique() if "city" in df.columns else 0
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{get_icon("area")}</div>
      <div class="kpi-number">{cities_count}</div>
      <div class="kpi-label">Cities / Districts</div>
    </div>
    """, unsafe_allow_html=True)
with m4:
    high_sev_count = int((df["severity"] == 3).sum())
    high_pct = round((high_sev_count / len(df)) * 100, 1) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{get_icon("alert")}</div>
      <div class="kpi-number">{high_pct}%</div>
      <div class="kpi-label">High Severity Ratio</div>
    </div>
    """, unsafe_allow_html=True)
with m5:
    night_count = int((df["time_of_day"] == "Night").sum())
    night_pct = round((night_count / len(df)) * 100, 1) if len(df) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{get_icon("clock")}</div>
      <div class="kpi-number">{night_pct}%</div>
      <div class="kpi-label">Night Incidents</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ANALYTICS TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "Category & Geographic Distribution",
    "Temporal & Time Patterns",
    "Environmental & Transport Context",
    "Detailed Data & Export",
])

# ── TAB 1: Category & Geography ──────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(an.chart_incidents_by_category(df), use_container_width=True)
    with c2:
        if "state" in df.columns and df["state"].nunique() > 1:
            st.plotly_chart(an.chart_incidents_by_state(df, top_n=10), use_container_width=True)
        else:
            st.plotly_chart(an.chart_incidents_by_area(df, top_n=10), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(an.chart_by_severity(df), use_container_width=True)
    with c4:
        st.plotly_chart(an.chart_incidents_by_area(df, top_n=10), use_container_width=True)

# ── TAB 2: Temporal & Time ───────────────────────────────────────────────────
with tab2:
    st.plotly_chart(an.chart_trend_over_time(df), use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.plotly_chart(an.chart_by_hour(df), use_container_width=True)
    with col_t2:
        st.plotly_chart(an.chart_by_day_of_week(df), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(an.chart_heatmap_hour_day(df), use_container_width=True)

# ── TAB 3: Environment & Transport ───────────────────────────────────────────
with tab3:
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.plotly_chart(an.chart_by_time_period(df), use_container_width=True)
    with col_e2:
        st.plotly_chart(an.chart_by_transport(df), use_container_width=True)

    if "lighting" in df.columns:
        light_counts = df["lighting"].value_counts().reset_index()
        light_counts.columns = ["Lighting Condition", "Count"]
        import plotly.express as px
        fig_light = px.bar(
            light_counts, x="Lighting Condition", y="Count",
            color="Count",
            color_continuous_scale=["#FCECF3", "#B9A7E8", "#7B5EA7"],
            text="Count",
        )
        fig_light.update_traces(textposition="outside")
        fig_light.update_layout(coloraxis_showscale=False)
        st.plotly_chart(an._apply_theme(fig_light, "Incidents by Ambient Lighting Condition"), use_container_width=True)

# ── TAB 4: Data & Export ─────────────────────────────────────────────────────
with tab4:
    st.markdown("### Filtered Dataset Inspection")
    disp_cols = [c for c in ["date", "state", "city", "area", "category", "severity_label", "hour", "time_of_day", "transport_mode", "lighting"] if c in df.columns]
    st.dataframe(df[disp_cols].head(300), width="stretch", hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Analytics Dataset (CSV)",
        data      = csv_data,
        file_name = "safeher_analytics_export.csv",
        mime      = "text/csv",
    )
    st.caption(f"Export includes all {len(df):,} filtered records with complete schema.")

# Footer disclaimer
st.markdown("""
<div class="clean-disclaimer">
  <strong>Analytical Disclaimer:</strong> The visualizations above reflect reported incident frequencies within the selected dataset.
  Variations across states and cities may stem from differing public reporting rates, local population densities, and reporting awareness.
</div>
""", unsafe_allow_html=True)
