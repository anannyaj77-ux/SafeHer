"""
test_suite.py – SafeHer automated verification suite
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

def main():
    print("=== 1. Testing geo_data ===")
    from geo_data import STATES_AND_UTS, get_all_states, get_cities_for_state, get_areas_for_city, search_locations
    states = get_all_states()
    assert len(states) == 36, f"Expected 36 states/UTs, got {len(states)}"
    assert "Delhi" in states and "Maharashtra" in states and "Tamil Nadu" in states
    cities_mh = get_cities_for_state("Maharashtra")
    assert "Mumbai" in cities_mh and "Pune" in cities_mh
    print(f"geo_data verified: 36 states/UTs, Maharashtra has {len(cities_mh)} cities.")

    print("=== 2. Testing data_processing and nationwide dataset ===")
    from data_processing import load_incidents, load_support_locations, get_summary_stats, filter_incidents, record_user_incident
    df, src = load_incidents()
    sup = load_support_locations()
    stats = get_summary_stats(df)
    assert len(df) >= 2000, f"Expected >=2000 incidents, got {len(df)}"
    assert len(sup) >= 100, f"Expected >=100 support locations, got {len(sup)}"
    assert stats["states"] == 36, f"Expected 36 states, got {stats['states']}"
    print(f"data_processing verified: {len(df)} incidents across {stats['states']} states and {stats['cities']} cities.")

    print("=== 3. Testing filter_incidents ===")
    filtered_delhi = filter_incidents(df, states=["Delhi"])
    assert len(filtered_delhi) > 0, "Delhi filter should return incidents"
    filtered_high = filter_incidents(df, severity=[3])
    assert len(filtered_high) > 0, "High severity filter should return incidents"
    print(f"Filters verified: {len(filtered_delhi)} Delhi incidents, {len(filtered_high)} high severity incidents.")

    print("=== 4. Testing mapping.py ===")
    from mapping import build_incident_map
    m = build_incident_map(df.head(50), sup.head(20), show_support=True, show_heatmap=True, show_clusters=True)
    assert m is not None, "Folium map should not be None"
    print("mapping.py verified: Folium map generated successfully.")

    print("=== 5. Testing analytics.py ===")
    import analytics as an
    f1 = an.chart_incidents_by_category(df)
    f2 = an.chart_incidents_by_state(df)
    f3 = an.chart_trend_over_time(df)
    f4 = an.chart_by_hour(df)
    f5 = an.chart_heatmap_hour_day(df)
    assert f1 and f2 and f3 and f4 and f5
    print("analytics.py verified: all Plotly charts generated successfully.")

    print("=== 6. Testing model_training.py and prediction ===")
    from model_training import train_all_models, predict_risk
    models = train_all_models(df)
    assert "Random Forest" in models
    assert "Logistic Regression" in models
    pred = predict_risk({"hour": 23, "severity": 3, "lighting": "Very Dark", "transport_mode": "Walking", "category": "Stalking"})
    assert pred in (0, 1), f"Expected 0 or 1 prediction, got {pred}"
    print(f"ML pipeline verified: Best model {models['_meta']['best_model']}, Risk prediction result: {pred}.")

    print("=== 7. Testing user incident reporting ===")
    success, msg = record_user_incident({
        "state": "Karnataka",
        "city": "Bengaluru",
        "area": "Indiranagar",
        "category": "Verbal Harassment",
        "severity": 2,
        "lighting": "Well-lit",
        "transport_mode": "Walking",
        "description": "Test verification report"
    })
    assert success, msg
    print("Incident reporting verified: User report recorded successfully.")

    print("\nALL BACKEND MODULES AND VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
