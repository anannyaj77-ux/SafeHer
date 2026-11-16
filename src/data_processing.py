"""
data_processing.py – SafeHer
Handles loading, validation, caching, cleaning, and filtering of datasets across India.
Integrates official National Crime Records Bureau (NCRB) statistics, verified emergency
support facilities, synthetic nationwide incident records, and session-based community reports.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import sys
import os

SRC_DIR  = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = ROOT_DIR / "data"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from geo_data import get_location_coordinates, STATES_AND_UTS, get_all_states

# ── Dataset Paths ─────────────────────────────────────────────────────────────
INCIDENTS_PATH        = DATA_DIR / "incidents.csv"
SUPPORT_LOCATIONS_PATH = DATA_DIR / "support_locations.csv"
VERIFIED_SUPPORT_PATH = DATA_DIR / "verified_support_facilities.csv"
NCRB_2022_PATH        = DATA_DIR / "ncrb_crime_against_women_2022.csv"
NCRB_2021_PATH        = DATA_DIR / "ncrb_crime_against_women_2021.csv"

# ── Dataset Provenance Metadata ──────────────────────────────────────────────
NCRB_METADATA = {
    "source_org": "National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of India",
    "report_name": "Crime in India 2022 (Volume 1, Chapter 3: Crimes Against Women)",
    "publication_date": "December 2023",
    "coverage": "All 28 States and 8 Union Territories of India",
    "reference_tables": "Table 3A.1 (Incidence & Crime Rates) and Table 3A.2 (Crime Head-wise Distribution)",
    "portal_url": "https://ncrb.gov.in/",
    "license_notes": "Published official government statistics for public awareness and policy evaluation.",
}

SUPPORT_FACILITY_METADATA = {
    "source_org": "Ministry of Women & Child Development / State Police Departments / Ministry of Health",
    "directory_name": "Emergency Support Infrastructure (Police Stations, District Hospitals, Sakhi One Stop Centres)",
    "coverage": "All 28 States and 8 Union Territories of India",
    "portal_url": "https://wcd.nic.in/schemes/sakhi-one-stop-centre-scheme",
}


# ── Incident Loading & Caching ───────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_incidents(path: Optional[Path] = None) -> Tuple[pd.DataFrame, str]:
    """
    Load the nationwide incidents dataset.
    Ensures datetime conversion and standard derived fields (severity_label, day_of_week).
    """
    target = Path(path) if path else INCIDENTS_PATH
    if not target.exists():
        from data_generation import save_datasets
        save_datasets(DATA_DIR)

    if target.exists():
        df = pd.read_csv(target)
    else:
        from data_generation import generate_synthetic_incidents
        df = generate_synthetic_incidents(2500)

    df = _standardize_incidents(df)
    return df, "demo"


def _standardize_incidents(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure consistent data types, dates, and labels across all incident records."""
    if df.empty:
        return df

    df = df.copy()

    # Parse date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Fill severity_label if missing
    if "severity_label" not in df.columns and "severity" in df.columns:
        sev_map = {1: "Low", 2: "Medium", 3: "High"}
        df["severity_label"] = df["severity"].map(sev_map).fillna("Medium")

    # Ensure temporal attributes
    if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
        if "day_of_week" not in df.columns:
            df["day_of_week"] = df["date"].dt.day_name()
        if "year" not in df.columns:
            df["year"] = df["date"].dt.year
        if "month" not in df.columns:
            df["month"] = df["date"].dt.month
        if "month_name" not in df.columns:
            df["month_name"] = df["date"].dt.strftime("%b %Y")

    # Ensure hour & time_of_day
    if "hour" in df.columns and "time_of_day" not in df.columns:
        df["time_of_day"] = df["hour"].apply(
            lambda h: "Night" if h < 6 else "Morning" if h < 12 else "Afternoon" if h < 17 else "Evening" if h < 20 else "Night"
        )

    return df


# ── Support Locations Loading & Caching ──────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_support_locations(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load nationwide emergency support facilities (Police Stations, Hospitals, Sakhi Centres).
    Loads 342 nationwide locations across all 36 States/UTs.
    """
    target = Path(path) if path else SUPPORT_LOCATIONS_PATH
    if target.exists():
        df = pd.read_csv(target)
        if len(df) >= 100:
            return df

    # Fallback to verified facilities if support_locations is unavailable
    if VERIFIED_SUPPORT_PATH.exists():
        df_v = pd.read_csv(VERIFIED_SUPPORT_PATH)
        if not df_v.empty:
            return df_v

    # Generate if not found
    from data_generation import generate_support_locations
    df = generate_support_locations()
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_verified_support_locations() -> pd.DataFrame:
    """Load officially verified police headquarters, major AIIMS/civil hospitals, and Sakhi centres."""
    if VERIFIED_SUPPORT_PATH.exists():
        return pd.read_csv(VERIFIED_SUPPORT_PATH)
    return load_support_locations()


@st.cache_data(ttl=3600, show_spinner=False)
def load_ncrb_data(year: int = 2022) -> pd.DataFrame:
    """Load authentic National Crime Records Bureau (NCRB) crime statistics."""
    target_path = NCRB_2022_PATH if year == 2022 else NCRB_2021_PATH
    if target_path.exists():
        return pd.read_csv(target_path)
    return pd.DataFrame()


def get_active_ncrb_summary() -> Dict[str, Any]:
    """Return verified national summary statistics from official NCRB records."""
    df_ncrb = load_ncrb_data(2022)
    if df_ncrb.empty:
        return {
            "total_cases": 445256,
            "national_rate": 66.4,
            "states_covered": 36,
            "top_state_volume": "Uttar Pradesh",
            "top_state_rate": "Delhi",
            "publication_year": "2022 (Published Dec 2023)",
            "source_org": NCRB_METADATA["source_org"],
        }
    return {
        "total_cases": int(df_ncrb["total_cases"].sum()),
        "national_rate": 66.4,
        "states_covered": len(df_ncrb),
        "top_state_volume": df_ncrb.sort_values("total_cases", ascending=False).iloc[0]["state"],
        "top_state_rate": df_ncrb.sort_values("rate_per_lakh", ascending=False).iloc[0]["state"],
        "publication_year": "2022 (Published Dec 2023)",
        "source_org": NCRB_METADATA["source_org"],
    }


# ── Safe Session State Fallback (for CLI tests & scripts) ────────────────────
_STANDALONE_SESSION_CACHE: Dict[str, Any] = {}

def _get_session_val(key: str, default: Any = None) -> Any:
    """Safely get session state variable whether inside Streamlit or standalone CLI."""
    try:
        return st.session_state.get(key, default)
    except Exception:
        return _STANDALONE_SESSION_CACHE.get(key, default)

def _set_session_val(key: str, val: Any) -> None:
    """Safely set session state variable whether inside Streamlit or standalone CLI."""
    try:
        st.session_state[key] = val
    except Exception:
        _STANDALONE_SESSION_CACHE[key] = val


# ── Active Incidents Provider ────────────────────────────────────────────────
def get_active_incidents() -> Tuple[pd.DataFrame, str]:
    """
    Return active dataset with provenance label ('demo' or 'uploaded').
    Integrates any user-submitted reports from the active session.
    """
    # 1. Custom user uploaded dataset
    uploaded = _get_session_val("safeher_uploaded_incidents")
    if isinstance(uploaded, pd.DataFrame) and not uploaded.empty:
        df = _standardize_incidents(uploaded.copy())
        # Append session reports if any
        user_reports = get_community_reports()
        if not user_reports.empty:
            df = pd.concat([user_reports, df], ignore_index=True)
        return df, "uploaded"

    # 2. Nationwide demo dataset
    df, src = load_incidents()
    df = df.copy()

    # Append session reports if any
    user_reports = get_community_reports()
    if not user_reports.empty:
        df = pd.concat([user_reports, df], ignore_index=True)

    return df, "demo"


# ── Summary KPIs ─────────────────────────────────────────────────────────────
def get_summary_stats(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Return high-level summary KPIs for the platform.
    Supplies all metric keys required across home dashboard, analytics, and verification.
    """
    if df is None or df.empty:
        df, _ = load_incidents()

    ncrb_summary = get_active_ncrb_summary()
    sup = load_support_locations()
    community_df = get_community_reports()

    total_count  = len(df)
    states_count = int(df["state"].nunique()) if "state" in df.columns else 36
    cities_count = int(df["city"].nunique()) if "city" in df.columns else 0
    areas_count  = int(df["area"].nunique()) if "area" in df.columns else 0
    high_sev     = int((df["severity"] == 3).sum()) if "severity" in df.columns else 0

    date_str = "2021 – 2026"
    if "date" in df.columns and not df.empty:
        valid_dates = df["date"].dropna()
        if not valid_dates.empty:
            try:
                min_d = valid_dates.min()
                max_d = valid_dates.max()
                if hasattr(min_d, "strftime") and hasattr(max_d, "strftime"):
                    date_str = f"{min_d.strftime('%b %Y')} – {max_d.strftime('%b %Y')}"
            except Exception:
                pass

    return {
        "total":               total_count,
        "states":              states_count,
        "cities":              cities_count,
        "areas":               areas_count,
        "high_severity":       high_sev,
        "date_range":          date_str,
        "total_ncrb_cases":    ncrb_summary["total_cases"],
        "national_crime_rate": ncrb_summary["national_rate"],
        "verified_facilities": len(sup),
        "community_reports":   len(community_df),
        "data_period":         date_str,
        "source_org":          ncrb_summary["source_org"],
    }


# ── Filtering Engine ──────────────────────────────────────────────────────────
def filter_incidents(
    df: pd.DataFrame,
    states:       Optional[List[str]] = None,
    cities:       Optional[List[str]] = None,
    areas:        Optional[List[str]] = None,
    categories:   Optional[List[str]] = None,
    time_periods: Optional[List[str]] = None,
    severity:     Optional[List[int]] = None,
    date_range:   Optional[Tuple[Any, Any]] = None,
) -> pd.DataFrame:
    """
    Robust multi-criteria filtering for incident records across India.
    Accepts scalar or list arguments and handles missing or empty columns gracefully.
    """
    if df.empty:
        return df.copy()

    sub = df.copy()

    # Filter states
    if states:
        if isinstance(states, str):
            states = [states]
        valid_states = [s for s in states if s and s != "All States & UTs"]
        if valid_states and "state" in sub.columns:
            sub = sub[sub["state"].isin(valid_states)]

    # Filter cities
    if cities:
        if isinstance(cities, str):
            cities = [cities]
        valid_cities = [c for c in cities if c and c not in ("All Cities", "All Districts / Cities")]
        if valid_cities and "city" in sub.columns:
            sub = sub[sub["city"].isin(valid_cities)]

    # Filter areas
    if areas:
        if isinstance(areas, str):
            areas = [areas]
        valid_areas = [a for a in areas if a and a not in ("All Areas", "All Localities")]
        if valid_areas and "area" in sub.columns:
            sub = sub[sub["area"].isin(valid_areas)]

    # Filter categories
    if categories and "category" in sub.columns:
        if isinstance(categories, str):
            categories = [categories]
        sub = sub[sub["category"].isin(categories)]

    # Filter time periods
    if time_periods and "time_of_day" in sub.columns:
        if isinstance(time_periods, str):
            time_periods = [time_periods]
        sub = sub[sub["time_of_day"].isin(time_periods)]

    # Filter severity
    if severity and "severity" in sub.columns:
        if isinstance(severity, int):
            severity = [severity]
        sub = sub[sub["severity"].isin(severity)]

    # Filter date range
    if date_range and len(date_range) == 2 and "date" in sub.columns:
        start_d, end_d = date_range
        if start_d is not None and end_d is not None:
            start_ts = pd.Timestamp(start_d)
            end_ts   = pd.Timestamp(end_d) + pd.Timedelta(days=1) - pd.Timedelta(nanoseconds=1)
            sub = sub[(sub["date"] >= start_ts) & (sub["date"] <= end_ts)]

    return sub


# ── Incident Reporting (Session-based) ───────────────────────────────────────
def record_user_incident(report: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Record an incident submitted by the user through the UI form.
    Immediately reflects in session analytics and map visualizations.
    """
    user_reports = _get_session_val("safeher_user_reports", [])
    if not isinstance(user_reports, list):
        user_reports = []

    required = ["category", "state", "city", "area", "severity"]
    missing = [k for k in required if not report.get(k)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    c_lat, c_lon = get_location_coordinates(report["state"], report["city"], report["area"])

    now = pd.Timestamp.now()
    hour = int(report.get("hour", now.hour))
    minute = int(report.get("minute", now.minute))

    time_of_day = (
        "Night"     if hour < 6  else
        "Morning"   if hour < 12 else
        "Afternoon" if hour < 17 else
        "Evening"   if hour < 20 else
        "Night"
    )

    sev = int(report["severity"])
    sev_label = {1: "Low", 2: "Medium", 3: "High"}.get(sev, "Medium")
    lighting = report.get("lighting", "Adequate")
    transport = report.get("transport_mode", "Other")

    risk_factors = 0
    if hour >= 20 or hour < 6:
        risk_factors += 2
    if lighting in ("Poorly-lit", "Very Dark"):
        risk_factors += 2
    if sev == 3:
        risk_factors += 2
    if report["category"] in ("Physical Harassment", "Stalking"):
        risk_factors += 1
    if transport in ("Walking", "Bus"):
        risk_factors += 1
    risk_label = 1 if risk_factors >= 4 else 0

    record = {
        "incident_id":       f"USR-{len(user_reports)+1:04d}",
        "date":              pd.Timestamp(report.get("date", now.strftime("%Y-%m-%d"))),
        "hour":              hour,
        "minute":            minute,
        "time_of_day":       time_of_day,
        "state":             report["state"],
        "city":              report["city"],
        "area":              report["area"],
        "latitude":          round(float(c_lat), 6),
        "longitude":         round(float(c_lon), 6),
        "category":          report["category"],
        "severity":          sev,
        "severity_label":    sev_label,
        "transport_mode":    transport,
        "lighting":          lighting,
        "reporting_channel": "App User Report",
        "victim_age_group":  report.get("victim_age_group", "Unspecified"),
        "risk_label":        risk_label,
        "description":       report.get("description", ""),
        "is_synthetic":      False,
        "is_user_report":    True,
        "year":              now.year,
        "month":             now.month,
        "month_name":        now.strftime("%b %Y"),
        "day_of_week":       now.day_name(),
    }

    user_reports.insert(0, record)
    _set_session_val("safeher_user_reports", user_reports)
    return True, "Incident report submitted successfully."


def record_community_incident(report: Dict[str, Any]) -> Tuple[bool, str]:
    """Compatibility alias for record_user_incident."""
    return record_user_incident(report)


def get_community_reports() -> pd.DataFrame:
    """Return all session-submitted incident reports as a DataFrame."""
    reports = _get_session_val("safeher_user_reports", [])
    if reports and isinstance(reports, list):
        return pd.DataFrame(reports)
    return pd.DataFrame()


# ── Custom CSV Validation & Cleaning ─────────────────────────────────────────
REQUIRED_COLUMNS = [
    "date", "category", "severity", "city", "area", "latitude", "longitude"
]

def validate_incident_columns(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that an uploaded CSV contains the required schema columns.
    """
    if df.empty:
        return False, "Uploaded file contains no records."

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}. Please verify CSV header."

    return True, "OK"


def validate_user_csv(df: pd.DataFrame) -> Tuple[bool, str]:
    """Compatibility alias for validate_incident_columns."""
    return validate_incident_columns(df)


def clean_incidents(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize user-uploaded incident datasets.
    Validates coordinates, converts datetimes, and adds derived columns.
    """
    if df.empty:
        return df

    cleaned = df.copy()

    # Parse date
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["date"])

    # Coordinate validation for India (approx. 6N-38N, 68E-98E)
    cleaned["latitude"]  = pd.to_numeric(cleaned["latitude"], errors="coerce")
    cleaned["longitude"] = pd.to_numeric(cleaned["longitude"], errors="coerce")
    cleaned = cleaned.dropna(subset=["latitude", "longitude"])
    cleaned = cleaned[(cleaned["latitude"].between(6.0, 38.0)) & (cleaned["longitude"].between(68.0, 98.0))]

    # Severity normalization
    cleaned["severity"] = pd.to_numeric(cleaned["severity"], errors="coerce").fillna(2).astype(int)
    cleaned["severity"] = cleaned["severity"].clip(1, 3)

    # Standardize string fields
    for col in ["category", "city", "area"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    if "state" not in cleaned.columns:
        cleaned["state"] = "Other / Unspecified"

    # Fill temporal attributes
    cleaned = _standardize_incidents(cleaned)

    # Risk label heuristic if missing
    if "risk_label" not in cleaned.columns:
        cleaned["risk_label"] = (cleaned["severity"] == 3).astype(int)

    return cleaned
