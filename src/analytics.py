"""
analytics.py – SafeHer
All Plotly chart-building functions.  Every chart uses the pastel purple/pink theme.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional

# ── Brand colours ─────────────────────────────────────────────────────────────
PALETTE = [
    "#B9A7E8",  # pastel purple   (primary)
    "#F2BFD1",  # soft pink       (secondary)
    "#D4B8F0",  # light violet
    "#F9D4E5",  # blush
    "#9B8DD4",  # deeper purple
    "#E8A8C4",  # rose
    "#C5B3EC",  # lavender mid
    "#FAC8D8",  # peach pink
]

THEME = dict(
    plot_bgcolor   = "#FDFBFF",
    paper_bgcolor  = "#FDFBFF",
    font_color     = "#392E4D",
    font_family    = "Inter, sans-serif",
)

AXIS_STYLE = dict(
    gridcolor      = "#E8DDF2",
    zerolinecolor  = "#E8DDF2",
    tickfont       = dict(color="#81768E", size=11),
    title_font     = dict(color="#392E4D", size=13),
)


def _apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title       = dict(text=title, font=dict(size=16, color="#392E4D"), x=0.01),
        legend      = dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#392E4D")),
        margin      = dict(l=40, r=20, t=50, b=40),
        hoverlabel  = dict(bgcolor="white", font_size=12, font_color="#392E4D"),
        **THEME,
    )
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


# ────────────────────────────────────────────────────────────────────────────
#  Bar charts
# ────────────────────────────────────────────────────────────────────────────
def chart_incidents_by_state(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    if df.empty or "state" not in df.columns:
        return _empty_fig("No data available")
    counts = df["state"].value_counts().nlargest(top_n).reset_index()
    counts.columns = ["State", "Count"]
    fig = px.bar(
        counts, x="State", y="Count",
        color="Count",
        color_continuous_scale=["#F2BFD1", "#B9A7E8", "#6C4FBF"],
        text="Count",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, xaxis=dict(tickangle=-30))
    return _apply_theme(fig, f"Top {top_n} States / UTs by Incident Count")


def chart_incidents_by_category(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("No data available")
    counts = df["category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]
    fig = px.bar(
        counts, x="Count", y="Category", orientation="h",
        color="Count",
        color_continuous_scale=["#F2BFD1", "#B9A7E8", "#6C4FBF"],
        text="Count",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
    return _apply_theme(fig, "Incidents by Category")


def chart_incidents_by_area(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    if df.empty:
        return _empty_fig("No data available")
    counts = df["area"].value_counts().nlargest(top_n).reset_index()
    counts.columns = ["Area", "Count"]
    fig = px.bar(
        counts, x="Area", y="Count",
        color="Count",
        color_continuous_scale=["#F9D4E5", "#B9A7E8", "#7B5EA7"],
        text="Count",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, xaxis=dict(tickangle=-35))
    return _apply_theme(fig, f"Top {top_n} Areas by Incident Count")


# ────────────────────────────────────────────────────────────────────────────
#  Time-series
# ────────────────────────────────────────────────────────────────────────────
def chart_trend_over_time(df: pd.DataFrame) -> go.Figure:
    if df.empty or "date" not in df.columns:
        return _empty_fig("No data available")
    try:
        monthly = df.resample("ME", on="date").size().reset_index(name="Count")
    except Exception:
        try:
            monthly = df.resample("M", on="date").size().reset_index(name="Count")
        except Exception:
            monthly = df.groupby(pd.Grouper(key="date", freq="M")).size().reset_index(name="Count")
    monthly.columns = ["Month", "Count"]
    fig = px.area(
        monthly, x="Month", y="Count",
        line_shape="spline",
        color_discrete_sequence=["#B9A7E8"],
    )
    fig.update_traces(
        fill="tozeroy",
        fillcolor="rgba(185,167,232,0.18)",
        line=dict(color="#9B8DD4", width=2.5),
    )
    return _apply_theme(fig, "Monthly Incident Trend")


def chart_by_hour(df: pd.DataFrame) -> go.Figure:
    if df.empty or "hour" not in df.columns:
        return _empty_fig("No data available")
    counts = df.groupby("hour").size().reindex(range(24), fill_value=0).reset_index()
    counts.columns = ["Hour", "Count"]
    fig = px.bar(
        counts, x="Hour", y="Count",
        color="Count",
        color_continuous_scale=["#F2BFD1", "#B9A7E8", "#6C4FBF"],
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", dtick=2, ticksuffix=":00"),
    )
    return _apply_theme(fig, "Incidents by Hour of Day")


def chart_by_day_of_week(df: pd.DataFrame) -> go.Figure:
    if df.empty or "day_of_week" not in df.columns:
        return _empty_fig("No data available")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = df["day_of_week"].value_counts().reindex(day_order, fill_value=0).reset_index()
    counts.columns = ["Day", "Count"]
    fig = px.bar(
        counts, x="Day", y="Count",
        color="Count",
        color_continuous_scale=["#F9D4E5", "#B9A7E8", "#7B5EA7"],
        text="Count",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig, "Incidents by Day of Week")


# ────────────────────────────────────────────────────────────────────────────
#  Pie / Donut
# ────────────────────────────────────────────────────────────────────────────
def chart_by_time_period(df: pd.DataFrame) -> go.Figure:
    if df.empty or "time_of_day" not in df.columns:
        return _empty_fig("No data available")
    counts = df["time_of_day"].value_counts().reset_index()
    counts.columns = ["Period", "Count"]
    fig = px.pie(
        counts, names="Period", values="Count",
        color_discrete_sequence=PALETTE,
        hole=0.45,
    )
    fig.update_traces(textposition="outside", textinfo="percent+label")
    return _apply_theme(fig, "Incidents by Time of Day")


def chart_by_severity(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("No data available")
    df = df.copy()
    if "severity_label" not in df.columns and "severity" in df.columns:
        df["severity_label"] = df["severity"].map({1: "Low", 2: "Medium", 3: "High"}).fillna("Medium")
    if "severity_label" not in df.columns:
        return _empty_fig("No data available")
    sev_map = {"Low": "#B9A7E8", "Medium": "#F2BFD1", "High": "#9B6EB0"}
    counts  = df["severity_label"].value_counts().reset_index()
    counts.columns = ["Severity", "Count"]
    fig = px.pie(
        counts, names="Severity", values="Count",
        color="Severity",
        color_discrete_map=sev_map,
        hole=0.45,
    )
    fig.update_traces(textposition="outside", textinfo="percent+label")
    return _apply_theme(fig, "Incidents by Severity")


def chart_by_transport(df: pd.DataFrame) -> go.Figure:
    if df.empty or "transport_mode" not in df.columns:
        return _empty_fig("No data available")
    counts = df["transport_mode"].value_counts().reset_index()
    counts.columns = ["Mode", "Count"]
    fig = px.bar(
        counts, x="Mode", y="Count",
        color="Count",
        color_continuous_scale=["#F2BFD1", "#B9A7E8", "#6C4FBF"],
        text="Count",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig, "Incidents by Transport Mode")


# ────────────────────────────────────────────────────────────────────────────
#  Area comparison
# ────────────────────────────────────────────────────────────────────────────
def chart_area_comparison(df: pd.DataFrame, selected_areas: list) -> go.Figure:
    if df.empty:
        return _empty_fig("No data available")
    sub = df[df["area"].isin(selected_areas)] if selected_areas else df
    counts = sub.groupby(["area", "category"]).size().reset_index(name="Count")
    fig = px.bar(
        counts, x="area", y="Count", color="category",
        barmode="group",
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(xaxis_title="Area", yaxis_title="Count", xaxis=dict(tickangle=-20))
    return _apply_theme(fig, "Category Breakdown by Area")


def chart_area_trend(df: pd.DataFrame, selected_areas: list) -> go.Figure:
    if df.empty or "date" not in df.columns:
        return _empty_fig("No data available")
    sub = df[df["area"].isin(selected_areas)] if selected_areas else df
    try:
        monthly = sub.groupby([pd.Grouper(key="date", freq="QE"), "area"]).size().reset_index(name="Count")
    except Exception:
        try:
            monthly = sub.groupby([pd.Grouper(key="date", freq="Q"), "area"]).size().reset_index(name="Count")
        except Exception:
            monthly = sub.groupby([pd.Grouper(key="date", freq="3M"), "area"]).size().reset_index(name="Count")
    fig = px.line(
        monthly, x="date", y="Count", color="area",
        line_shape="spline",
        color_discrete_sequence=PALETTE,
        markers=True,
    )
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Incidents")
    return _apply_theme(fig, "Quarterly Trend by Area")


def chart_heatmap_hour_day(df: pd.DataFrame) -> go.Figure:
    """Heatmap of incidents by hour × day of week."""
    if df.empty:
        return _empty_fig("No data available")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = df.groupby(["day_of_week", "hour"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(day_order, fill_value=0)
    pivot = pivot.reindex(columns=range(24), fill_value=0)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h:02d}:00" for h in range(24)],
        y=day_order,
        colorscale=[
            [0.0,  "#FDF6FF"],
            [0.35, "#D4B8F0"],
            [0.70, "#B9A7E8"],
            [1.0,  "#6C4FBF"],
        ],
        showscale=True,
        hovertemplate="Day: %{y}<br>Hour: %{x}<br>Count: %{z}<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="")
    return _apply_theme(fig, "Incident Heatmap – Hour × Day of Week")


# ────────────────────────────────────────────────────────────────────────────
#  ML / Model charts
# ────────────────────────────────────────────────────────────────────────────
def chart_confusion_matrix(cm: np.ndarray) -> go.Figure:
    labels = ["Lower Risk", "Higher Risk"]
    fig = px.imshow(
        cm, text_auto=True, x=labels, y=labels,
        color_continuous_scale=["#FDF6FF", "#B9A7E8", "#6C4FBF"],
        aspect="auto",
    )
    fig.update_layout(
        xaxis_title="Predicted", yaxis_title="Actual",
        coloraxis_showscale=False,
    )
    return _apply_theme(fig, "Confusion Matrix")


def chart_feature_importance(feature_names: list, importances: np.ndarray) -> go.Figure:
    df_fi = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    df_fi.sort_values("Importance", ascending=True, inplace=True)
    fig = px.bar(
        df_fi, x="Importance", y="Feature", orientation="h",
        color="Importance",
        color_continuous_scale=["#F2BFD1", "#B9A7E8", "#6C4FBF"],
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_theme(fig, "Feature Importance")


def chart_model_comparison(results: dict) -> go.Figure:
    """Bar chart comparing model metrics side by side."""
    rows = []
    for model_name, metrics in results.items():
        for metric_name, value in metrics.items():
            rows.append({"Model": model_name, "Metric": metric_name, "Value": round(value, 4)})
    df_r = pd.DataFrame(rows)
    fig = px.bar(
        df_r, x="Model", y="Value", color="Metric",
        barmode="group",
        color_discrete_sequence=PALETTE,
        text_auto=".3f",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis=dict(range=[0, 1.15]))
    return _apply_theme(fig, "Model Comparison")


# ── Utilities ─────────────────────────────────────────────────────────────────
def _empty_fig(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#81768E"),
    )
    fig.update_layout(**THEME, xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig
