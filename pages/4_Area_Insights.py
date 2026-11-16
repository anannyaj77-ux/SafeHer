"""
pages/4_Area_Insights.py – SafeHer: Area Insights
Multi-area comparative safety analysis: incident volume, category distributions,
temporal trends, data completeness indices, and contextual reporting caveats.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd
import html
import plotly.express as px

from data_processing import get_active_incidents, filter_incidents
import analytics as an
from geo_data import get_all_states, get_cities_for_state, get_areas_for_city
from ui_components import get_global_css, get_icon

# ── Page config ────────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "Area Insights – SafeHer",
    page_icon  = icon_path,
    layout     = "wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:10px;">
    {get_icon("area")} Comparative Neighbourhood Intelligence
  </div>
  <h1 class="page-header-title">Area Insights & Comparison</h1>
  <p class="page-header-desc">
    Compare safety indicators across states, districts, and neighbourhoods in India.
    Incident counts indicate reported frequencies within the dataset and must be interpreted
    alongside local reporting factors.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df, _source = get_active_incidents()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {get_icon('search')} Geographic Selection", unsafe_allow_html=True)
    st.markdown("---")

    all_states = ["All States & UTs"] + sorted(df["state"].dropna().unique().tolist()) if "state" in df.columns else ["All States & UTs"]
    sel_state = st.selectbox("State / Union Territory", all_states, index=0)

    if sel_state != "All States & UTs" and "state" in df.columns:
        city_pool = sorted(df[df["state"] == sel_state]["city"].dropna().unique().tolist())
    else:
        city_pool = sorted(df["city"].dropna().unique().tolist())

    sel_city = st.selectbox("District / City", ["All Cities"] + city_pool, index=0)

    # Determine Area Pool
    sub_df = df.copy()
    if sel_state != "All States & UTs" and "state" in sub_df.columns:
        sub_df = sub_df[sub_df["state"] == sel_state]
    if sel_city != "All Cities":
        sub_df = sub_df[sub_df["city"] == sel_city]

    area_pool = sorted(sub_df["area"].dropna().unique().tolist())
    default_areas = area_pool[:4] if len(area_pool) >= 4 else area_pool

    sel_areas = st.multiselect(
        "Select Localities to Compare (Max 6)",
        options=area_pool,
        default=default_areas,
        max_selections=6,
        help="Select between 2 and 6 localities to examine side by side."
    )

    st.markdown("---")
    min_d = df["date"].min().date() if not df.empty else pd.Timestamp("2021-01-01").date()
    max_d = df["date"].max().date() if not df.empty else pd.Timestamp.now().date()
    date_range = st.date_input("Date Period", (min_d, max_d), min_value=min_d, max_value=max_d)

# ── Filter Data ────────────────────────────────────────────────────────────────
sub = df.copy()
if sel_state != "All States & UTs" and "state" in sub.columns:
    sub = sub[sub["state"] == sel_state]
if sel_city != "All Cities":
    sub = sub[sub["city"] == sel_city]
if len(date_range) == 2:
    sub = sub[(sub["date"] >= pd.Timestamp(date_range[0])) & (sub["date"] <= pd.Timestamp(date_range[1]))]

if sel_areas:
    sub_areas = sub[sub["area"].isin(sel_areas)]
else:
    sub_areas = sub

if sub_areas.empty:
    st.warning("No records found for the selected localities and date period. Please broaden the selection in the sidebar.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  AREA SUMMARY CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Locality Comparative Summary")

area_stats = []
max_count  = 0
target_areas = sel_areas if sel_areas else sub_areas["area"].unique()[:6]

for area in target_areas:
    area_df = sub_areas[sub_areas["area"] == area]
    count   = len(area_df)
    max_count = max(max_count, count)
    high_sev  = int((area_df["severity"] == 3).sum())
    night_pct = (area_df["time_of_day"] == "Night").mean() * 100 if count else 0
    top_cat   = area_df["category"].mode()[0] if count else "N/A"

    context_cols = [c for c in ("lighting", "transport_mode", "reporting_channel") if c in area_df.columns]
    completeness = area_df[context_cols].notna().all(axis=1).mean() * 100 if count and context_cols else 0
    area_stats.append({
        "area": area,
        "count": count,
        "high_sev": high_sev,
        "night_pct": round(night_pct, 1),
        "top_cat": top_cat,
        "completeness": round(completeness, 1),
    })

card_cols = st.columns(min(len(area_stats), 3))
for i, stat in enumerate(area_stats):
    with card_cols[i % 3]:
        fill_pct = (stat["count"] / max_count * 100) if max_count else 0
        comp_color = (
            "#27AE60" if stat["completeness"] >= 85 else
            "#E67E22" if stat["completeness"] >= 60 else "#C0392B"
        )
        comp_label = "High" if stat["completeness"] >= 85 else "Moderate" if stat["completeness"] >= 60 else "Partial"

        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:14px;padding:20px;box-shadow:0 2px 8px rgba(185,167,232,0.10);margin-bottom:14px;">
          <div style="font-size:1.1rem;font-weight:700;color:#392E4D;display:flex;align-items:center;gap:6px;">
            {get_icon("pin")}
            <span>{html.escape(str(stat['area']))}</span>
          </div>
          <div style="font-size:0.84rem;color:#6D6180;margin:6px 0 10px 0;line-height:1.5;">
            <b>{stat['count']:,}</b> reports &nbsp;·&nbsp;
            <b>{stat['high_sev']}</b> high severity &nbsp;·&nbsp;
            <b>{stat['night_pct']}%</b> night
          </div>
          <div style="font-size:0.82rem;color:#7B5EA7;margin-bottom:8px;">
            Most Frequent Category: <b>{html.escape(str(stat['top_cat']))}</b>
          </div>
          <div style="background:#F5F0FF;border-radius:6px;height:7px;margin:8px 0;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#B9A7E8,#F2BFD1);height:7px;width:{fill_pct:.0f}%;"></div>
          </div>
          <div style="margin-top:8px;">
            <span style="display:inline-block;border-radius:20px;padding:3px 10px;font-size:0.75rem;font-weight:600;background:{comp_color}18;color:{comp_color};border:1px solid {comp_color}44;">
              {comp_label} context data coverage ({stat['completeness']}%)
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="clean-disclaimer">
  <strong>Reporting Sensitivity Notice:</strong> Higher incident counts in an area may reflect higher public reporting propensity, active local helplines, or transit density rather than absolute danger.
  Raw volume counts should not be conflated with per-capita crime rates.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  COMPARATIVE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
t1, t2, t3 = st.tabs([
    "Category Breakdown Across Localities",
    "Quarterly Incident Trends",
    "Time of Day Comparison",
])

with t1:
    st.plotly_chart(
        an.chart_area_comparison(sub_areas, list(target_areas)),
        use_container_width=True,
    )

with t2:
    st.plotly_chart(
        an.chart_area_trend(sub_areas, list(target_areas)),
        use_container_width=True,
    )

with t3:
    pivot = (
        sub_areas.groupby(["area", "time_of_day"]).size().reset_index(name="Count")
        if not sub_areas.empty else pd.DataFrame()
    )
    if not pivot.empty:
        fig_t = px.bar(
            pivot, x="area", y="Count", color="time_of_day",
            barmode="group",
            color_discrete_sequence=["#B9A7E8", "#F2BFD1", "#9B8DD4", "#FAC8D8"],
            title="Incident Distribution by Time Period across Selected Localities",
        )
        fig_t.update_layout(
            plot_bgcolor="#FDFBFF", paper_bgcolor="#FDFBFF",
            font_color="#392E4D", xaxis_title="Locality",
        )
        st.plotly_chart(fig_t, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DATA TABLE & EXPORT
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("Summary Metrics Table & Export", expanded=False):
    df_summary = pd.DataFrame(area_stats).rename(columns={
        "area": "Locality", "count": "Reported Incidents",
        "high_sev": "High Severity Incidents", "night_pct": "Night Reports (%)",
        "top_cat": "Most Reported Category", "completeness": "Context Completeness (%)"
    })
    st.dataframe(df_summary, width="stretch", hide_index=True)

    csv_summary = df_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Area Summary Report (CSV)",
        data      = csv_summary,
        file_name = "safeher_area_insights_summary.csv",
        mime      = "text/csv",
    )

# Footer
st.markdown("""
<div class="clean-disclaimer" style="margin-top:24px;">
  <strong>Data Notice:</strong> All metrics shown are based on the active dataset. Demonstration data is labelled DEMO DATA.
  In an immediate emergency in India, contact <strong>112</strong>.
</div>
""", unsafe_allow_html=True)
