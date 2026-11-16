"""
pages/5_Emergency_Support.py – SafeHer: Emergency Support
Verified pan-India emergency helplines, state-specific safety contacts,
direct calling actions, nearby support facilities, trusted contacts, and safety planning.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import html
import urllib.parse
import pandas as pd

from data_processing import load_support_locations
from geo_data import STATES_AND_UTS, get_all_states, get_cities_for_state, get_state_info
from ui_components import get_global_css, get_icon

# ── Page config ────────────────────────────────────────────────────────────────
icon_path = str(ROOT / "assets" / "safeher_icon.png") if (ROOT / "assets" / "safeher_icon.png").exists() else None
st.set_page_config(
    page_title = "Emergency Support – SafeHer",
    page_icon  = icon_path,
    layout     = "wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="status-pill" style="margin-bottom:10px;">
    {get_icon("phone")} Crisis Response & Safety Directory
  </div>
  <h1 class="page-header-title">Emergency Support & Helplines</h1>
  <p class="page-header-desc">
    Rapid access to verified national and state emergency response numbers, nearby support infrastructure,
    trusted contact alerts, and personal safety preparedness across India.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Immediate Emergency Banner ────────────────────────────────────────────────
st.markdown(f"""
<div class="emergency-banner-bar" style="text-align:center;padding:24px;">
  <div style="display:inline-flex;padding:10px;background:#FFFFFF;border-radius:50%;margin-bottom:8px;box-shadow:0 2px 8px rgba(185,167,232,0.15);">
    {get_icon("alert")}
  </div>
  <div style="font-size:1.55rem;font-weight:800;color:#A92646;margin-bottom:6px;">
    Immediate Emergency Response: Dial 112
  </div>
  <div style="color:#6B4E57;font-size:0.95rem;max-width:720px;margin:0 auto 16px auto;line-height:1.6;">
    112 is India's single pan-India Emergency Response Support System (ERSS) coordinating police,
    medical ambulances, fire response, and disaster management 24 hours a day.
  </div>
  <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
    <a href="tel:112" class="sos-link-btn" style="background:#C0392B;color:white!important;border-color:#A92646;">Direct Call 112</a>
    <a href="tel:181" class="sos-link-btn" style="background:#7B5EA7;color:white!important;border-color:#63438E;">Call Women Helpline 181</a>
    <a href="tel:1091" class="sos-link-btn" style="background:#2980B9;color:white!important;border-color:#1B4F72;">Call Women Police 1091</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NATIONAL HELPLINES DIRECTORY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("phone")} National Emergency Helplines</div>', unsafe_allow_html=True)
st.caption("All numbers are official toll-free services provided by the Government of India.")

national_helplines = [
    ("112", "Emergency Response Support System (ERSS)", "All-India emergency response uniting police, fire, health, and rescue.", "https://112.gov.in/"),
    ("181", "Women Helpline (Ministry of WCD)", "24-hour toll-free crisis intervention, counseling, and referral for women facing violence.", "https://www.india.gov.in/directory/helpline"),
    ("1091", "Women in Distress (Police Special Cell)", "Dedicated police patrol and distress dispatch for women.", "https://mha.gov.in/"),
    ("14490", "National Commission for Women (NCW)", "NCW 24/7 dedicated helpline for women in distress and legal assistance.", "https://ncwapps.nic.in/frmContactUS.aspx"),
    ("1930", "National Cyber Crime Reporting", "Helpline for reporting online harassment, stalking, deepfakes, and cyber threats.", "https://cybercrime.gov.in/"),
    ("1098", "Childline (Integrated with ERSS 112)", "Emergency assistance, rescue, and protection for minors and young girls.", "https://www.wcd.gov.in/child/child-helpline"),
]

h_cols = st.columns(3)
for idx, (num, name, desc, portal_url) in enumerate(national_helplines):
    with h_cols[idx % 3]:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:14px;padding:18px;box-shadow:0 2px 8px rgba(185,167,232,0.10);margin-bottom:14px;height:100%;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <div style="font-size:1.8rem;font-weight:800;color:#7B5EA7;line-height:1.1;">{num}</div>
            <div style="font-size:0.95rem;font-weight:700;color:#392E4D;margin:6px 0 4px 0;">{name}</div>
            <div style="font-size:0.83rem;color:#6D6180;line-height:1.5;">{desc}</div>
          </div>
          <div style="margin-top:14px;padding-top:10px;border-top:1px solid #F5F0FF;display:flex;justify-content:space-between;align-items:center;">
            <a href="tel:{num}" style="font-size:0.82rem;font-weight:700;color:#7B5EA7;text-decoration:none;">Call Now</a>
            <a href="{portal_url}" target="_blank" rel="noopener noreferrer" style="font-size:0.78rem;color:#9B8DD4;text-decoration:none;">Official Portal</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STATE & UNION TERRITORY SPECIFIC DIRECTORY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("shield")} State & Union Territory Safety Directory</div>', unsafe_allow_html=True)

c_s1, c_s2 = st.columns([1, 2])
with c_s1:
    selected_state = st.selectbox("Select State or Union Territory", get_all_states(), key="state_emergency_sel")
    s_info = get_state_info(selected_state)

with c_s2:
    if s_info:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:14px;padding:20px;box-shadow:0 2px 8px rgba(185,167,232,0.10);">
          <div style="font-size:1.2rem;font-weight:700;color:#392E4D;margin-bottom:8px;">
            {selected_state} Emergency Information
          </div>
          <div style="font-size:0.86rem;color:#6D6180;line-height:1.7;">
            <div>Administrative Capital: <b>{s_info['capital']}</b></div>
            <div>Jurisdiction Type: <b>{s_info['type']}</b></div>
            <div>Primary Emergency Dispatch: <b>112 (ERSS)</b></div>
            <div>Dedicated State Women Helpline: <b style="color:#7B5EA7;">{s_info.get('helpline', '112 / 181')}</b></div>
          </div>
          <div style="margin-top:12px;">
            <a href="tel:112" style="display:inline-block;background:#F5F0FF;border:1px solid #B9A7E8;color:#392E4D;padding:6px 14px;border-radius:8px;font-size:0.82rem;font-weight:600;text-decoration:none;">Connect to {selected_state} Control Room</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NEARBY EMERGENCY INFRASTRUCTURE DIRECTORY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("hospital")} Nearby Emergency Support Facilities</div>', unsafe_allow_html=True)
st.markdown("<p style='font-size:0.88rem;color:#6D6180;'>Locate police stations, general civil hospitals, and Sakhi One Stop Centres across India.</p>", unsafe_allow_html=True)

df_support = load_support_locations()

f_c1, f_c2, f_c3 = st.columns(3)
with f_c1:
    sup_state = st.selectbox("Filter by State / UT", ["All States & UTs"] + get_all_states(), index=0, key="sup_state_filter")
with f_c2:
    if sup_state != "All States & UTs":
        sup_cities = ["All Cities"] + get_cities_for_state(sup_state)
    else:
        sup_cities = ["All Cities"] + sorted(df_support["city"].dropna().unique().tolist())
    sup_city = st.selectbox("Filter by District / City", sup_cities, index=0, key="sup_city_filter")
with f_c3:
    sup_type = st.selectbox("Facility Type", ["All Facilities", "Police Station", "Hospital", "Women Help Centre"], index=0)

filtered_sup = df_support.copy()
if sup_state != "All States & UTs":
    filtered_sup = filtered_sup[filtered_sup["state"] == sup_state]
if sup_city != "All Cities":
    filtered_sup = filtered_sup[filtered_sup["city"] == sup_city]
if sup_type != "All Facilities":
    if sup_type == "Women Help Centre":
        filtered_sup = filtered_sup[filtered_sup["type"].isin(["Women Help Centre", "Sakhi One Stop Centre"])]
    else:
        filtered_sup = filtered_sup[filtered_sup["type"] == sup_type]

if filtered_sup.empty:
    st.info("No facilities found matching the selected filter criteria.")
else:
    # Display top 6 in cards with direct navigation links
    st.caption(f"Showing {min(len(filtered_sup), 6)} of {len(filtered_sup)} facilities:")
    sup_cols = st.columns(3)
    for idx, (_, fac) in enumerate(filtered_sup.head(6).iterrows()):
        fac_name = html.escape(str(fac.get("name", "Facility")))
        fac_type = html.escape(str(fac.get("type", "Support")))
        fac_city = html.escape(str(fac.get("city", "")))
        fac_area = html.escape(str(fac.get("area", "")))
        fac_phone = html.escape(str(fac.get("phone", "112")))
        fac_lat = fac.get("latitude")
        fac_lon = fac.get("longitude")
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={fac_lat},{fac_lon}" if fac_lat and fac_lon else "#"

        with sup_cols[idx % 3]:
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:16px;box-shadow:0 1px 6px rgba(185,167,232,0.08);margin-bottom:12px;">
              <div style="font-weight:700;color:#392E4D;font-size:0.95rem;margin-bottom:4px;">{fac_name}</div>
              <div style="font-size:0.78rem;font-weight:600;color:#7B5EA7;margin-bottom:6px;">{fac_type}</div>
              <div style="font-size:0.82rem;color:#6D6180;margin-bottom:8px;">{fac_area}, {fac_city}</div>
              <div style="font-size:0.8rem;color:#392E4D;margin-bottom:10px;">Contact: <b>{fac_phone}</b></div>
              <a href="{gmaps_link}" target="_blank" rel="noopener noreferrer" style="font-size:0.8rem;color:#7B5EA7;font-weight:600;text-decoration:none;">Open in Google Maps</a>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TRUSTED CONTACTS MANAGER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("phone")} Personal Trusted Contacts</div>', unsafe_allow_html=True)
st.caption("Store up to 5 personal emergency contacts in your active browser session. Contact numbers are stored locally and never transmitted to external servers.")

if "trusted_contacts" not in st.session_state:
    st.session_state.trusted_contacts = []

with st.expander("Add a Trusted Contact", expanded=len(st.session_state.trusted_contacts) == 0):
    with st.form("trusted_contact_form", clear_on_submit=True):
        tc1, tc2, tc3 = st.columns([2, 2, 1.2])
        with tc1:
            tc_name = st.text_input("Full Name", placeholder="e.g., Ananya Sharma")
        with tc2:
            tc_phone = st.text_input("Phone Number", placeholder="e.g., 9876543210")
        with tc3:
            tc_rel = st.selectbox("Relationship", ["Family", "Friend", "Colleague", "Neighbor", "Other"])

        add_btn = st.form_submit_button("Save Contact")
        if add_btn:
            digits = "".join(c for c in tc_phone if c.isdigit())
            if not tc_name.strip() or not tc_phone.strip():
                st.error("Please enter both contact name and phone number.")
            elif len(digits) < 10:
                st.error("Please enter a valid 10-digit phone number.")
            elif len(st.session_state.trusted_contacts) >= 5:
                st.error("Maximum 5 contacts allowed. Remove an existing contact to add another.")
            else:
                st.session_state.trusted_contacts.append({
                    "name": tc_name.strip(),
                    "phone": digits,
                    "relation": tc_rel,
                })
                st.success(f"{tc_name.strip()} saved to trusted contacts.")
                st.rerun()

if st.session_state.trusted_contacts:
    for idx, contact in enumerate(st.session_state.trusted_contacts):
        col_c, col_act = st.columns([4, 1.5])
        with col_c:
            safe_name = html.escape(contact["name"])
            safe_rel  = html.escape(contact["relation"])
            phone_num = contact["phone"]
            wa_text = urllib.parse.quote(f"EMERGENCY ALERT: Hi {contact['name']}, I am using SafeHer. I may need assistance. Please check on me or call.")
            wa_link = f"https://wa.me/91{phone_num}?text={wa_text}"
            tel_link = f"tel:{phone_num}"

            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-radius:12px;padding:14px 18px;margin-bottom:8px;box-shadow:0 1px 6px rgba(185,167,232,0.08);">
              <b style="color:#392E4D;font-size:1rem;">{safe_name}</b>
              <span style="color:#7B5EA7;font-size:0.8rem;margin-left:8px;font-weight:600;">({safe_rel})</span>
              <div style="color:#6D6180;font-size:0.84rem;margin-top:4px;">
                Phone: +91 {phone_num} &nbsp;·&nbsp;
                <a href="{tel_link}" style="color:#7B5EA7;font-weight:600;text-decoration:none;">Call</a> &nbsp;|&nbsp;
                <a href="{wa_link}" target="_blank" rel="noopener noreferrer" style="color:#27AE60;font-weight:600;text-decoration:none;">Send WhatsApp SOS</a>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col_act:
            if st.button("Remove", key=f"del_tc_{idx}", help="Remove contact"):
                st.session_state.trusted_contacts.pop(idx)
                st.rerun()
else:
    st.info("No personal trusted contacts registered yet. Add contacts above for quick SOS dialing and WhatsApp alert dispatch.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SAFETY PLANNING CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("check")} Personal Safety Preparedness Checklist</div>', unsafe_allow_html=True)
st.caption("Review these key safety habits. Checklist selections are for personal verification.")

checklist_items = [
    ("ice_contacts", "I have at least 3 emergency contacts designated as 'ICE' (In Case of Emergency) on my phone lock screen."),
    ("route_sharing", "Before traveling late at night, I share my expected route, cab details, and ETA with a trusted person."),
    ("pan_india_112", "I have memorized and speed-dialed 112 as India's unified emergency number."),
    ("charged_device", "My mobile device is adequately charged and has battery-saver shortcuts configured before transit."),
    ("local_landmarks", "I am familiar with nearest 24/7 locations (police stations, open hospitals, transit junctions) along my frequent routes."),
    ("live_tracking", "I know how to initiate live location sharing via WhatsApp or Google Maps during solo travel."),
    ("trust_instincts", "If a situation or route feels unsafe, I proactively alter my path, enter a well-lit establishment, or seek assistance immediately."),
]

for key, text in checklist_items:
    st.checkbox(text, key=f"prep_check_{key}")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  OFFICIAL GOVERNMENT INITIATIVES & APPS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'<div class="section-heading-custom">{get_icon("info")} Official Security Resources & Portals</div>', unsafe_allow_html=True)

govt_resources = [
    ("ERSS 112 India Portal", "https://112.gov.in/", "Government pan-India single emergency response support system with mobile emergency app."),
    ("National Commission for Women (NCW)", "https://ncw.nic.in/", "Statutory body addressing rights violations, complaints, and legal aid for women."),
    ("Sakhi One Stop Centre Scheme", "https://wcd.nic.in/schemes/sakhi-one-stop-centre-scheme", "Integrated support including medical aid, police assistance, counseling, and shelter under one roof."),
    ("National Cyber Crime Reporting Portal", "https://cybercrime.gov.in/", "Dedicated portal for reporting cyber harassment, online stalking, and privacy breaches."),
    ("Ministry of Women and Child Development", "https://wcd.nic.in/", "Government policies, welfare programs, and helpline guidelines."),
]

g_cols = st.columns(2)
for idx, (res_name, res_url, res_desc) in enumerate(govt_resources):
    with g_cols[idx % 2]:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #E8DDF2;border-left:4px solid #B9A7E8;border-radius:10px;padding:14px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(185,167,232,0.06);">
          <a href="{res_url}" target="_blank" rel="noopener noreferrer" style="color:#7B5EA7;font-weight:700;font-size:0.95rem;text-decoration:none;">{res_name}</a>
          <div style="color:#6D6180;font-size:0.83rem;margin-top:4px;line-height:1.5;">{res_desc}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer disclaimer
st.markdown("""
<div class="clean-disclaimer" style="margin-top:24px;">
  <strong>Important Safety Directive:</strong> SafeHer is an awareness and analytical software platform.
  It does not possess automated dispatcher authority or intercept emergency communications.
  In any acute physical emergency or threatening situation anywhere in India, dial <strong>112</strong> immediately.
</div>
""", unsafe_allow_html=True)
