"""
mapping.py – SafeHer
Interactive Folium maps for nationwide women-safety analysis across India.
Displays incident clusters, heatmaps, verified emergency support infrastructure,
and official state-level NCRB indicators.
"""

import folium
import html
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
from typing import Optional, Tuple

FACILITY_COLORS = {
    "Police Station":        "darkblue",
    "Hospital":              "green",
    "Women Help Centre":     "purple",
    "Sakhi One Stop Centre": "purple",
}

FACILITY_ICONS = {
    "Police Station":        "shield-alt",
    "Hospital":              "plus-circle",
    "Women Help Centre":     "hands-helping",
    "Sakhi One Stop Centre": "hands-helping",
}


def _display(value) -> str:
    """Escape untrusted text before embedding it in HTML."""
    if pd.isna(value) or value is None:
        return "Not Specified"
    return html.escape(str(value))


def _incident_popup(row: pd.Series) -> str:
    """Render popup for an incident record."""
    cat = _display(row.get("category"))
    date_str = str(row.get("date", "N/A"))[:10]
    time_of_day = _display(row.get("time_of_day", ""))
    sev = int(row.get("severity", 2))
    sev_label = _display(row.get("severity_label", {1: "Low", 2: "Medium", 3: "High"}.get(sev, "Medium")))
    city = _display(row.get("city", ""))
    area = _display(row.get("area", ""))
    state = _display(row.get("state", ""))
    lighting = _display(row.get("lighting", "Not Specified"))
    transport = _display(row.get("transport_mode", "Not Specified"))
    is_synth = bool(row.get("is_synthetic", True))

    badge_bg = "#FADBD8" if sev == 3 else "#FCF3CF" if sev == 2 else "#D4EFDF"
    badge_color = "#922B21" if sev == 3 else "#7D6608" if sev == 2 else "#1E8449"
    synth_badge = """<span style="background:#F5EEF8;color:#6C3483;border:1px solid #D7BDE2;padding:2px 6px;border-radius:4px;font-size:9px;font-weight:700;">DEMO DATA</span>""" if is_synth else """<span style="background:#E8F8F5;color:#117A65;border:1px solid #A3E4D7;padding:2px 6px;border-radius:4px;font-size:9px;font-weight:700;">USER REPORT</span>"""

    return f"""
    <div style="font-family:'Inter',system-ui,sans-serif;min-width:220px;padding:6px;color:#392E4D;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <span style="font-weight:700;font-size:13px;color:#392E4D;">{cat}</span>
        {synth_badge}
      </div>
      <div style="margin-bottom:6px;">
        <span style="background:{badge_bg};color:{badge_color};padding:2px 8px;border-radius:8px;font-size:10px;font-weight:700;">
          Severity {sev} ({sev_label})
        </span>
      </div>
      <div style="font-size:11px;color:#554868;line-height:1.6;">
        <div><b>Location:</b> {area}, {city} ({state})</div>
        <div><b>Date & Time:</b> {date_str} · {time_of_day}</div>
        <div><b>Transport:</b> {transport}</div>
        <div><b>Lighting:</b> {lighting}</div>
      </div>
    </div>
    """


def _verified_facility_popup(row: pd.Series) -> str:
    """Render popup for a police, hospital, or Sakhi centre."""
    name = _display(row.get("name"))
    ftype = _display(row.get("type"))
    state = _display(row.get("state"))
    city = _display(row.get("city"))
    addr = _display(row.get("address", row.get("area", "")))
    phone = _display(row.get("phone"))
    lat, lon = row.get("latitude"), row.get("longitude")

    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else "#"

    return f"""
    <div style="font-family:'Inter',system-ui,sans-serif;min-width:240px;padding:6px;color:#392E4D;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <span style="font-weight:700;font-size:13px;color:#392E4D;">{name}</span>
      </div>
      <div style="margin-bottom:6px;">
        <span style="background:#E8F8F5;color:#117A65;border:1px solid #A3E4D7;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;letter-spacing:0.04em;">
          EMERGENCY INFRASTRUCTURE
        </span>
      </div>
      <div style="font-size:11px;color:#7B5EA7;font-weight:600;margin-bottom:4px;">
        {ftype} · {city}, {state}
      </div>
      <div style="font-size:11px;color:#615575;line-height:1.5;margin-bottom:6px;">
        Address: {addr}
      </div>
      <hr style="border:none;border-top:1px solid #E8DDF2;margin:6px 0;">
      <div style="font-size:11px;color:#392E4D;margin-bottom:6px;">
        Helpline / Contact: <b>{phone}</b>
      </div>
      <div style="margin-top:6px;font-size:11px;">
        <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" style="color:#7B5EA7;font-weight:700;text-decoration:none;">Open in Google Maps</a>
      </div>
    </div>
    """


def _state_ncrb_popup(row: pd.Series) -> str:
    """Render popup for an official State/UT NCRB crime summary marker."""
    state = _display(row.get("state"))
    total = f"{int(row.get('total_cases', 0)):,}"
    rate = f"{float(row.get('rate_per_lakh', 0)):.1f}"
    pop = f"{float(row.get('female_pop_lakhs', 0)):.1f} Lakhs" if "female_pop_lakhs" in row else "Published Census"

    return f"""
    <div style="font-family:'Inter',system-ui,sans-serif;min-width:230px;padding:6px;color:#392E4D;">
      <div style="font-weight:700;font-size:13px;color:#392E4D;margin-bottom:4px;">
        {state}
      </div>
      <div style="margin-bottom:6px;">
        <span style="background:#F5F0FF;color:#63438E;border:1px solid #B9A7E8;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;">
          NCRB 2022 OFFICIAL DATA
        </span>
      </div>
      <div style="font-size:11px;line-height:1.6;color:#554868;">
        <div>Total Crimes Against Women (2022): <b>{total}</b></div>
        <div>Rate per Lakh Women: <b>{rate}</b> (National: 66.4)</div>
        <div>Female Population Base: <b>{pop}</b></div>
      </div>
      <hr style="border:none;border-top:1px solid #E8DDF2;margin:6px 0;">
      <div style="font-size:10px;color:#81768E;">
        Source: National Crime Records Bureau (NCRB), MHA
      </div>
    </div>
    """


def build_incident_map(
    incidents:     pd.DataFrame,
    support:       Optional[pd.DataFrame] = None,
    show_support:  bool = True,
    show_heatmap:  bool = False,
    show_clusters: bool = True,
    center_lat:    float = 22.9734,
    center_lon:    float = 78.6569,
    zoom:          int   = 5,
    user_location: Optional[Tuple[float, float]] = None,
) -> folium.Map:
    """
    Build comprehensive Folium safety map with incidents, clusters, density heatmaps,
    support facilities, and user location reference.
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # ── User Current Location Pin (if provided) ──────────────────────────────
    if user_location and len(user_location) == 2:
        u_lat, u_lon = user_location
        if not (pd.isna(u_lat) or pd.isna(u_lon)):
            folium.Marker(
                location=[u_lat, u_lon],
                popup=folium.Popup(
                    """
                    <div style="font-family:'Inter',sans-serif;font-size:12px;color:#392E4D;padding:4px;">
                      <b>Your Specified Location</b><br>
                      <span style="color:#7B5EA7;font-size:11px;">Reference coordinate for nearby facilities</span>
                    </div>
                    """,
                    max_width=220,
                ),
                tooltip="Your Specified Location",
                icon=folium.Icon(color="red", icon="crosshairs", prefix="fa"),
            ).add_to(m)

            folium.Circle(
                location=[u_lat, u_lon],
                radius=3000,
                color="#E89BBB",
                fill=True,
                fill_color="#F2BFD1",
                fill_opacity=0.2,
            ).add_to(m)

    # ── Incident Density Heatmap Layer ────────────────────────────────────────
    if show_heatmap and incidents is not None and not incidents.empty:
        heat_coords = incidents[["latitude", "longitude"]].dropna().values.tolist()
        if heat_coords:
            HeatMap(
                heat_coords,
                radius=20,
                blur=15,
                gradient={"0.2": "#FCECF3", "0.5": "#B9A7E8", "0.8": "#E67E22", "1.0": "#C0392B"},
                name="Incident Density Heatmap",
            ).add_to(m)

    # ── Reported Incident Markers Layer ───────────────────────────────────────
    if incidents is not None and not incidents.empty:
        inc_group = folium.FeatureGroup(name="Reported Incidents", show=True)
        target_container = MarkerCluster(name="Incident Clusters").add_to(inc_group) if show_clusters else inc_group

        for _, row in incidents.iterrows():
            lat, lon = row.get("latitude"), row.get("longitude")
            if pd.isna(lat) or pd.isna(lon):
                continue

            sev = int(row.get("severity", 2))
            marker_color = "red" if sev == 3 else "orange" if sev == 2 else "green"
            icon_name = "exclamation-triangle" if sev == 3 else "exclamation" if sev == 2 else "info-circle"

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(_incident_popup(row), max_width=280),
                tooltip=f"{row.get('category')} ({row.get('area', '')}, {row.get('city', '')})",
                icon=folium.Icon(color=marker_color, icon=icon_name, prefix="fa"),
            ).add_to(target_container)

        inc_group.add_to(m)

    # ── Emergency Support Facilities Layer ───────────────────────────────────
    if show_support and support is not None and not support.empty:
        fac_group = folium.FeatureGroup(name="Support Infrastructure", show=True)
        fac_cluster = MarkerCluster(name="Support Facilities").add_to(fac_group)

        for _, row in support.iterrows():
            lat, lon = row.get("latitude"), row.get("longitude")
            if pd.isna(lat) or pd.isna(lon):
                continue
            ftype = row.get("type", "Hospital")
            color = FACILITY_COLORS.get(ftype, "blue")
            icon_name = FACILITY_ICONS.get(ftype, "info-circle")

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(_verified_facility_popup(row), max_width=290),
                tooltip=f"{row.get('name')} ({ftype})",
                icon=folium.Icon(color=color, icon=icon_name, prefix="fa"),
            ).add_to(fac_cluster)

        fac_group.add_to(m)

    _add_provenance_legend(m)
    folium.LayerControl(position="topright", collapsed=True).add_to(m)
    return m


def _add_provenance_legend(m: folium.Map):
    """Add a stylish floating legend to the Folium map."""
    legend_html = """
    <div style="position:fixed;bottom:24px;left:14px;z-index:9999;
                background:rgba(255,255,255,0.96);padding:14px 18px;
                border-radius:14px;font-family:'Inter',system-ui,sans-serif;
                font-size:11px;color:#392E4D;
                box-shadow:0 3px 14px rgba(185,167,232,0.25);
                border:1px solid #E8DDF2;line-height:1.6;">
      <div style="font-weight:700;font-size:12px;margin-bottom:6px;color:#392E4D;">Map Legend</div>
      <div><span style="display:inline-block;width:10px;height:10px;background:#C0392B;margin-right:6px;border-radius:50%;"></span>High Severity Incident (3)</div>
      <div><span style="display:inline-block;width:10px;height:10px;background:#E67E22;margin-right:6px;border-radius:50%;"></span>Medium Severity Incident (2)</div>
      <div><span style="display:inline-block;width:10px;height:10px;background:#27AE60;margin-right:6px;border-radius:50%;"></span>Low Severity Incident (1)</div>
      <hr style="border:none;border-top:1px solid #E8DDF2;margin:6px 0;">
      <div><span style="display:inline-block;width:10px;height:10px;background:#1A5276;margin-right:6px;border-radius:2px;"></span>Police Stations</div>
      <div><span style="display:inline-block;width:10px;height:10px;background:#1E8449;margin-right:6px;border-radius:2px;"></span>Hospitals / Medical Response</div>
      <div><span style="display:inline-block;width:10px;height:10px;background:#7D3C98;margin-right:6px;border-radius:2px;"></span>Sakhi One Stop / Women Centres</div>
      <div style="margin-top:6px;font-size:10px;color:#81768E;">Basemap: © OpenStreetMap</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))


# Compatibility alias
def build_nationwide_safety_map(
    support_df:       pd.DataFrame,
    ncrb_df:          Optional[pd.DataFrame] = None,
    community_df:     Optional[pd.DataFrame] = None,
    demo_df:          Optional[pd.DataFrame] = None,
    show_facilities:  bool = True,
    show_ncrb_states: bool = True,
    show_community:   bool = True,
    show_heatmap:     bool = False,
    center_lat:       float = 22.9734,
    center_lon:       float = 78.6569,
    zoom:             int   = 5,
    user_location:    Optional[Tuple[float, float]] = None,
) -> folium.Map:
    """Wrapper supporting the legacy call signature."""
    active_incidents = community_df if community_df is not None and not community_df.empty else demo_df
    if active_incidents is None:
        from data_processing import get_active_incidents
        active_incidents, _ = get_active_incidents()

    return build_incident_map(
        incidents     = active_incidents,
        support       = support_df,
        show_support  = show_facilities,
        show_heatmap  = show_heatmap,
        show_clusters = True,
        center_lat    = center_lat,
        center_lon    = center_lon,
        zoom          = zoom,
        user_location = user_location,
    )
