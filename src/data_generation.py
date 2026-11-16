"""
data_generation.py – SafeHer
Generates a realistic synthetic nationwide dataset of women-safety incidents
and emergency support locations across all 28 Indian States and 8 Union Territories.

NOTE: All generated records are synthetic for demonstration, educational,
and analytical purposes. No real-world incident victims or confidential records are represented.
All records are explicitly tagged with is_synthetic=True and DEMO DATA.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import random
import sys

# Ensure geo_data is importable
SRC_DIR = Path(__file__).parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from geo_data import STATES_AND_UTS, get_all_states

# ── Reproducibility ─────────────────────────────────────────────────────────
SEED = 42
rng  = np.random.default_rng(SEED)
random.seed(SEED)

# ── Configuration ────────────────────────────────────────────────────────────
INCIDENT_CATEGORIES = [
    "Verbal Harassment",
    "Physical Harassment",
    "Stalking",
    "Eve Teasing",
    "Theft / Snatching",
    "Unsafe Environment",
    "Online Harassment",
    "Domestic Dispute",
]

TRANSPORT_MODES = ["Bus", "Auto", "Metro", "Walking", "Cab", "Train", "Two-Wheeler", "Other"]
LIGHTING_CONDITIONS = ["Well-lit", "Poorly-lit", "Adequate", "Very Dark"]
REPORTING_CHANNELS  = ["Police Station", "Helpline 112", "Women Helpline 181", "App Report", "Online Portal", "NGO"]
VICTIM_AGE_GROUPS   = ["15-20", "21-25", "26-30", "31-35", "36-40", "41-50", "51+"]


def generate_synthetic_incidents(n: int = 2500) -> pd.DataFrame:
    """
    Generate ``n`` synthetic incident records distributed across all 28 States and 8 UTs of India.
    Uses authentic geographic centers and coordinates.
    """
    records = []
    all_states = get_all_states()

    # Relative population/urbanization weight for realistic density distribution
    high_pop_states = ["Uttar Pradesh", "Maharashtra", "West Bengal", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan", "Telangana", "Kerala", "Bihar", "Madhya Pradesh"]
    weights = []
    for s in all_states:
        if s in high_pop_states:
            weights.append(3.0)
        elif STATES_AND_UTS[s]["type"] == "Union Territory":
            weights.append(1.0)
        else:
            weights.append(1.8)
    weights = np.array(weights, dtype=float)
    weights /= weights.sum()

    date_start = pd.Timestamp("2021-01-01")
    date_end   = pd.Timestamp("2026-10-31")
    date_range_days = max(1, (date_end - date_start).days)

    # Hour distribution: peaks at evening/night (18-22) and morning rush (7-9)
    hour_weights = np.array([1, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 4, 5, 6, 6, 5, 4, 3], dtype=float)
    hour_weights /= hour_weights.sum()

    for i in range(n):
        # Pick state
        state = rng.choice(all_states, p=weights)
        sdata = STATES_AND_UTS[state]
        cities = list(sdata["cities"].keys())
        city = rng.choice(cities)
        cdata = sdata["cities"][city]
        area = rng.choice(cdata["areas"])
        base_lat, base_lon = cdata["center"]

        # Small coordinate jitter within ~1.5 km for realistic locality scatter
        lat = float(base_lat + rng.uniform(-0.02, 0.02))
        lon = float(base_lon + rng.uniform(-0.02, 0.02))

        # Date & time
        incident_date = date_start + pd.Timedelta(days=int(rng.integers(0, date_range_days)))
        hour = int(rng.choice(24, p=hour_weights))
        minute = int(rng.integers(0, 60))

        time_of_day = (
            "Night"     if hour < 6  else
            "Morning"   if hour < 12 else
            "Afternoon" if hour < 17 else
            "Evening"   if hour < 20 else
            "Night"
        )

        category  = rng.choice(INCIDENT_CATEGORIES)
        severity  = int(rng.choice([1, 2, 3], p=[0.25, 0.50, 0.25]))  # 1=Low, 2=Med, 3=High
        transport = rng.choice(TRANSPORT_MODES)
        lighting  = rng.choice(LIGHTING_CONDITIONS)
        channel   = rng.choice(REPORTING_CHANNELS)
        age_group = rng.choice(VICTIM_AGE_GROUPS)

        # Synthetic risk label (0=lower relative risk, 1=higher relative risk)
        risk_factors = 0
        if hour >= 20 or hour < 6:
            risk_factors += 2
        if lighting in ("Poorly-lit", "Very Dark"):
            risk_factors += 2
        if severity == 3:
            risk_factors += 2
        if category in ("Physical Harassment", "Stalking"):
            risk_factors += 1
        if transport in ("Walking", "Bus"):
            risk_factors += 1
        risk_label = 1 if risk_factors >= 4 else 0

        records.append({
            "incident_id":       f"INC-{i+1:05d}",
            "date":              incident_date.strftime("%Y-%m-%d"),
            "hour":              hour,
            "minute":            minute,
            "time_of_day":       time_of_day,
            "state":             state,
            "city":              city,
            "area":              area,
            "latitude":          round(lat, 6),
            "longitude":         round(lon, 6),
            "category":          category,
            "severity":          severity,
            "transport_mode":    transport,
            "lighting":          lighting,
            "reporting_channel": channel,
            "victim_age_group":  age_group,
            "risk_label":        risk_label,
            "is_synthetic":      True,
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b %Y")
    df["day_of_week"] = df["date"].dt.day_name()
    return df


def generate_support_locations() -> pd.DataFrame:
    """
    Return a DataFrame of synthetic and verified support resources across India.
    Includes Police Stations, General Hospitals, Women Help Centres, and Sakhi One Stop Centres.
    """
    locations = []

    for state, sdata in STATES_AND_UTS.items():
        for city, cdata in sdata["cities"].items():
            base_lat, base_lon = cdata["center"]
            helpline = sdata.get("helpline", "112")

            # 1. City / District Main Police Station
            locations.append({
                "name":         f"{city} Central Police Station",
                "type":         "Police Station",
                "state":        state,
                "city":         city,
                "area":         cdata["areas"][0] if cdata["areas"] else city,
                "latitude":     round(base_lat + rng.uniform(-0.012, 0.012), 6),
                "longitude":    round(base_lon + rng.uniform(-0.012, 0.012), 6),
                "phone":        f"Emergency: 112 / State: {helpline}",
                "is_synthetic": True,
            })

            # 2. General / District Hospital
            locations.append({
                "name":         f"{city} District Civil Hospital",
                "type":         "Hospital",
                "state":        state,
                "city":         city,
                "area":         cdata["areas"][1] if len(cdata["areas"]) > 1 else city,
                "latitude":     round(base_lat + rng.uniform(-0.015, 0.015), 6),
                "longitude":    round(base_lon + rng.uniform(-0.015, 0.015), 6),
                "phone":        "Emergency: 112 / Ambulance: 108",
                "is_synthetic": True,
            })

            # 3. Women Help Centre / Sakhi One Stop Centre
            locations.append({
                "name":         f"{city} Sakhi One Stop Centre",
                "type":         "Women Help Centre",
                "state":        state,
                "city":         city,
                "area":         cdata["areas"][-1] if cdata["areas"] else city,
                "latitude":     round(base_lat + rng.uniform(-0.010, 0.010), 6),
                "longitude":    round(base_lon + rng.uniform(-0.010, 0.010), 6),
                "phone":        f"Helpline: 181 / Women Helpline",
                "is_synthetic": True,
            })

    return pd.DataFrame(locations)


def save_datasets(data_dir: Path, force_nationwide: bool = False):
    """
    Generate and save datasets. If the existing incidents file lacks nationwide coverage,
    regenerate it.
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    incidents_path = data_dir / "incidents.csv"
    support_path   = data_dir / "support_locations.csv"

    need_incidents = not incidents_path.exists() or force_nationwide
    if not need_incidents:
        try:
            sample_df = pd.read_csv(incidents_path, nrows=10)
            if "state" not in sample_df.columns:
                need_incidents = True
        except Exception:
            need_incidents = True

    if need_incidents:
        df_incidents = generate_synthetic_incidents(2500)
        df_incidents.to_csv(incidents_path, index=False)
        print(f"[DataGen] Saved {len(df_incidents)} nationwide incidents -> {incidents_path}")

    need_support = not support_path.exists() or force_nationwide
    if not need_support:
        try:
            sample_sup = pd.read_csv(support_path, nrows=10)
            if "state" not in sample_sup.columns:
                need_support = True
        except Exception:
            need_support = True

    if need_support:
        df_support = generate_support_locations()
        df_support.to_csv(support_path, index=False)
        print(f"[DataGen] Saved {len(df_support)} nationwide support locations -> {support_path}")


if __name__ == "__main__":
    save_datasets(Path("data"), force_nationwide=True)
