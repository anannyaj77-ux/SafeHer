"""
pages/1_Safety_Map.py – SafeHer: Nationwide Safety Map
Interactive geospatial mapping with nationwide Indian coverage, incident clusters,
heatmaps, emergency support locations, and geolocation capabilities.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from data_processing import get_active_incidents, load_support_locations, filter_incidents
from mapping import build_incident_map
from geo_data import (
    STATES_AND_UTS, get_all_states, get_cities_for_state,
    get_areas_for_city, get_location_coordinates, search_locations,
)
from ui_components import get_global_css, get_icon

# ── Page config ────────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "Safety Map – SafeHer",
    page_icon  = icon_path,
    layout     = "wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df_all, source = get_active_incidents()
df_support     = load_support_locations()

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:10px;">
    {get_icon("map")} Geospatial Intelligence System
  </div>
  <h1 class="page-header-title">Nationwide Safety Map</h1>
  <p class="page-header-desc">
    Explore reported safety patterns, incident concentration heatmaps, and verified emergency support
    infrastructure across all 28 Indian States and 8 Union Territories.
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR: NATIONWIDE FILTERS & CONTROLS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"### {get_icon('search')} Location & Filters", unsafe_allow_html=True)
    st.markdown("---")

    # Fast Location Search
    search_q = st.text_input("Quick Location Search", placeholder="Type city, state, or area...", help="Search any Indian state, city, or locality")
    searched_coords = None
    if search_q:
        search_results = search_locations(search_q)
        if search_results:
            st.caption(f"Found {len(search_results)} matches across India:")
            selected_match = st.selectbox(
                "Select Search Result",
                options=search_results,
                format_func=lambda x: f"{x['name']} ({x['type']} - {x['state']})",
                key="map_search_select"
            )
            if selected_match:
                searched_coords = selected_match["coords"]

    st.markdown("---")
    st.markdown("**Nationwide Geographic Filter**")

    # 1. State / UT Selection
    all_states = ["All States & UTs"] + get_all_states()
    sel_state = st.selectbox("State / Union Territory", all_states, index=0)

    # 2. Dynamic City / District Selection
    if sel_state != "All States & UTs":
        state_cities = get_cities_for_state(sel_state)
        avail_cities = ["All Districts / Cities"] + state_cities
    else:
        avail_cities = ["All Districts / Cities"] + sorted(df_all["city"].dropna().unique().tolist())

    sel_city = st.selectbox("District / City", avail_cities, index=0)

    # 3. Dynamic Locality Selection
    if sel_state != "All States & UTs" and sel_city != "All Districts / Cities":
        city_areas = get_areas_for_city(sel_state, sel_city)
        avail_areas = ["All Localities"] + city_areas
    else:
        avail_areas = ["All Localities"] + sorted(df_all["area"].dropna().unique().tolist())

    sel_area = st.selectbox("Locality / Sector", avail_areas, index=0)

    st.markdown("---")
    st.markdown("**Incident Attributes**")

    all_cats = sorted(df_all["category"].dropna().unique().tolist())
    sel_cats = st.multiselect("Category", all_cats, default=None)

    all_periods = ["Morning", "Afternoon", "Evening", "Night"]
    sel_periods = st.multiselect("Time of Day", all_periods, default=None)

    min_date = df_all["date"].min().date() if not df_all.empty else pd.Timestamp("2021-01-01").date()
    max_date = df_all["date"].max().date() if not df_all.empty else pd.Timestamp.now().date()
    date_range = st.date_input("Date Period", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("---")
    st.markdown(f"### {get_icon('locate')} Current Location Simulation", unsafe_allow_html=True)
    enable_user_loc = st.checkbox("Simulate Current Location Pin", value=False)
    user_coords = None
    if enable_user_loc:
        uc1, uc2 = st.columns(2)
        with uc1:
            u_lat = st.number_input("Latitude", value=28.6139, format="%.4f")
        with uc2:
            u_lon = st.number_input("Longitude", value=77.2090, format="%.4f")
        user_coords = (u_lat, u_lon)
        st.caption("A red location pin with radius is rendered on the map.")

    st.markdown("---")
    st.markdown("### Display Layers")
    show_heatmap  = st.toggle("Incident Density Heatmap", value=True)
    show_support  = st.toggle("Support Infrastructure (Police / Hospitals)", value=True)
    show_clusters = st.toggle("Cluster Nearby Incidents", value=True)

    max_markers = st.slider("Map marker display limit", 100, 1500, 500, step=100,
                            help="Limits markers on the browser client for optimal rendering performance.")

# ══════════════════════════════════════════════════════════════════════════════
#  APPLY FILTERS
# ══════════════════════════════════════════════════════════════════════════════
filter_states = [sel_state] if sel_state != "All States & UTs" else None
filter_cities = [sel_city] if sel_city != "All Districts / Cities" else None
filter_areas  = [sel_area] if sel_area != "All Localities" else None

df_filtered = filter_incidents(
    df_all,
    states       = filter_states,
    cities       = filter_cities,
    areas        = filter_areas,
    categories   = sel_cats or None,
    time_periods = sel_periods or None,
    date_range   = (date_range[0], date_range[1]) if len(date_range) == 2 else None,
)

# Filter support locations
df_sup_filtered = df_support.copy()
if filter_states:
    df_sup_filtered = df_sup_filtered[df_sup_filtered["state"].isin(filter_states)]
if filter_cities:
    df_sup_filtered = df_sup_filtered[df_sup_filtered["city"].isin(filter_cities)]

# Sample for map performance
if len(df_filtered) > max_markers:
    df_map = df_filtered.sample(max_markers, random_state=42)
    sampled = True
else:
    df_map  = df_filtered
    sampled = False

# Determine Map Center and Zoom level
if searched_coords:
    center_lat, center_lon = searched_coords
    zoom = 12
elif sel_area != "All Localities" and not df_filtered.empty:
    center_lat = float(df_filtered["latitude"].mean())
    center_lon = float(df_filtered["longitude"].mean())
    zoom = 13
elif sel_city != "All Districts / Cities" and sel_state != "All States & UTs":
    c_lat, c_lon = get_location_coordinates(sel_state, sel_city)
    center_lat, center_lon = c_lat, c_lon
    zoom = 11
elif sel_state != "All States & UTs":
    s_lat, s_lon = get_location_coordinates(sel_state)
    center_lat, center_lon = s_lat, s_lon
    zoom = 7
else:
    center_lat = 22.9734  # Geographic center of India
    center_lon = 78.6569
    zoom = 5

# ══════════════════════════════════════════════════════════════════════════════
#  STATS ROW
# ══════════════════════════════════════════════════════════════════════════════
s_c1, s_c2, s_c3, s_c4 = st.columns(4)
with s_c1:
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:12px 16px;box-shadow:0 1px 6px rgba(185,167,232,0.08);">
      <div style="font-size:0.75rem;color:#81768E;font-weight:600;text-transform:uppercase;">Incidents in Filter</div>
      <div style="font-size:1.45rem;font-weight:700;color:#7B5EA7;">{len(df_filtered):,}</div>
    </div>
    """, unsafe_allow_html=True)
with s_c2:
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:12px 16px;box-shadow:0 1px 6px rgba(185,167,232,0.08);">
      <div style="font-size:0.75rem;color:#81768E;font-weight:600;text-transform:uppercase;">Plotted on Map</div>
      <div style="font-size:1.45rem;font-weight:700;color:#392E4D;">{len(df_map):,}</div>
    </div>
    """, unsafe_allow_html=True)
with s_c3:
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:12px 16px;box-shadow:0 1px 6px rgba(185,167,232,0.08);">
      <div style="font-size:0.75rem;color:#81768E;font-weight:600;text-transform:uppercase;">Support Infrastructure</div>
      <div style="font-size:1.45rem;font-weight:700;color:#27AE60;">{len(df_sup_filtered):,}</div>
    </div>
    """, unsafe_allow_html=True)
with s_c4:
    high_count = int((df_filtered["severity"] == 3).sum()) if not df_filtered.empty else 0
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:12px 16px;box-shadow:0 1px 6px rgba(185,167,232,0.08);">
      <div style="font-size:0.75rem;color:#81768E;font-weight:600;text-transform:uppercase;">High Severity Reports</div>
      <div style="font-size:1.45rem;font-weight:700;color:#C0392B;">{high_count:,}</div>
    </div>
    """, unsafe_allow_html=True)

if sampled:
    st.info(f"Displaying {max_markers} of {len(df_filtered):,} filtered incidents for smooth interactive performance. Adjust the slider in the sidebar to render more.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE FOLIUM MAP
# ══════════════════════════════════════════════════════════════════════════════
if df_filtered.empty and not enable_user_loc:
    st.warning("No incidents match the active filters. Expand your geographic selection or date range in the sidebar.")
else:
    with st.spinner("Rendering interactive geospatial layers…"):
        fmap = build_incident_map(
            incidents     = df_map,
            support       = df_sup_filtered if show_support else pd.DataFrame(),
            show_support  = show_support,
            show_heatmap  = show_heatmap,
            show_clusters = show_clusters,
            center_lat    = center_lat,
            center_lon    = center_lon,
            zoom          = zoom,
            user_location = user_coords,
        )
        st_folium(fmap, use_container_width=True, height=620, returned_objects=[])

# ══════════════════════════════════════════════════════════════════════════════
#  DIRECTORY & DATA TABLES
# ══════════════════════════════════════════════════════════════════════════════
t1, t2 = st.tabs(["Nearby Emergency Support Directory", "Filtered Incident Records"])

with t1:
    if df_sup_filtered.empty:
        st.info("No support units found for the selected geographic filter.")
    else:
        disp_cols = ["name", "type", "state", "city", "area", "phone"]
        avail_sup = [c for c in disp_cols if c in df_sup_filtered.columns]
        styled_sup = df_sup_filtered[avail_sup].rename(columns={
            "name": "Facility Name", "type": "Facility Type",
            "state": "State / UT", "city": "City / District",
            "area": "Locality", "phone": "Helpline Contact"
        })
        st.dataframe(styled_sup, width="stretch", hide_index=True)
        st.caption("Demonstration support locations are based on verified administrative centers. Always confirm directly with local emergency authorities.")

with t2:
    if df_filtered.empty:
        st.info("No records matching the filter criteria.")
    else:
        show_cols = ["date", "state", "city", "area", "category", "severity_label",
                     "time_of_day", "transport_mode", "lighting"]
        avail_inc = [c for c in show_cols if c in df_filtered.columns]
        st.dataframe(df_filtered[avail_inc].head(250), width="stretch", hide_index=True)

        csv = df_filtered[avail_inc].to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered Incident Records (CSV)",
            data      = csv,
            file_name = "safeher_nationwide_incidents.csv",
            mime      = "text/csv",
        )
        st.caption(f"Showing first 250 of {len(df_filtered):,} filtered records.")

# Footer disclaimer
st.markdown("""
<div class="clean-disclaimer" style="margin-top:24px;">
  <strong>Geospatial Notice:</strong> Coordinates and support locations are provided for safety planning and awareness.
  Demonstration datasets are clearly labelled as DEMO DATA. For immediate emergencies anywhere in India, call <strong>112</strong> immediately.
</div>
""", unsafe_allow_html=True)
