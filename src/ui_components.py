"""
ui_components.py – SafeHer
Reusable UI components, SVG icons, and styling utilities for the SafeHer platform.
All decorative emojis are replaced with clean, modern SVG vector icons.
"""

# Reusable SVG Icons in SafeHer lavender / pink palette
SVG_ICONS = {
    "shield": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>""",
    "map": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>""",
    "analytics": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>""",
    "brain": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04z"></path><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04z"></path></svg>""",
    "area": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>""",
    "phone": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C0392B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>""",
    "search": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>""",
    "pin": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>""",
    "info": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>""",
    "alert": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C0392B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>""",
    "check": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#27AE60" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>""",
    "clock": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>""",
    "calendar": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>""",
    "hospital": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#27AE60" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>""",
    "police": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2980B9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5.25-3.5 10-8 12-4.5-2-8-6.75-8-12V6l8-4z"></path></svg>""",
    "plus": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>""",
    "trash": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C0392B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>""",
    "locate": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7B5EA7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="22" y1="12" x2="18" y2="12"></line><line x1="6" y1="12" x2="2" y2="12"></line><line x1="12" y1="6" x2="12" y2="2"></line><line x1="12" y1="22" x2="12" y2="18"></line></svg>""",
}


def get_icon(name: str) -> str:
    """Return raw inline SVG string for the specified icon name."""
    return SVG_ICONS.get(name, "")


def get_global_css() -> str:
    """Return unified, modern lavender & blush-pink CSS design system."""
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

      html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }

      /* Base layout background */
      .stApp {
        background-color: #FAF7FD !important;
      }

      .main .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px;
      }

      /* Sidebar aesthetic */
      section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F0FF 0%, #FDF4F8 100%) !important;
        border-right: 1px solid #E8DDF2 !important;
      }

      /* Modern Page Header */
      .page-header {
        background: linear-gradient(135deg, #EDE6FF 0%, #FCECF3 70%, #F5E6FF 100%);
        border-radius: 18px;
        padding: 24px 32px;
        margin-bottom: 24px;
        border: 1px solid #E8DDF2;
        box-shadow: 0 2px 12px rgba(185,167,232,0.10);
      }
      .page-header-title {
        color: #392E4D;
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .page-header-desc {
        color: #6D6180;
        font-size: 0.95rem;
        line-height: 1.55;
        margin: 0;
      }

      /* KPI Cards */
      .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E8DDF2;
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(185,167,232,0.10);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(185,167,232,0.22);
      }
      .kpi-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #F5F0FF;
        margin-bottom: 8px;
      }
      .kpi-number {
        font-size: 2.1rem;
        font-weight: 700;
        color: #7B5EA7;
        line-height: 1.15;
      }
      .kpi-label {
        font-size: 0.8rem;
        color: #7E7292;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
      }

      /* Feature / Navigation Cards */
      .nav-card {
        background: #FFFFFF;
        border: 1px solid #E8DDF2;
        border-radius: 16px;
        padding: 24px 20px;
        height: 100%;
        box-shadow: 0 2px 12px rgba(185,167,232,0.10);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
      }
      .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(185,167,232,0.22);
        border-color: #B9A7E8;
      }
      .nav-card-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #F5F0FF, #FCECF3);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 14px;
        border: 1px solid #E8DDF2;
      }
      .nav-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #392E4D;
        margin-bottom: 8px;
      }
      .nav-card-desc {
        font-size: 0.86rem;
        color: #6D6180;
        line-height: 1.55;
      }

      /* Emergency Banner */
      .emergency-banner-bar {
        background: linear-gradient(135deg, #FFE8F0 0%, #FFF2F7 100%);
        border: 1.5px solid #F2BFD1;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 3px 14px rgba(242,191,209,0.25);
      }
      .emergency-banner-title {
        color: #A92646;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
      }
      .emergency-banner-sub {
        color: #6B4E57;
        font-size: 0.9rem;
        line-height: 1.5;
      }

      /* Buttons */
      .stButton > button {
        background: linear-gradient(135deg, #B9A7E8, #CDB4E8) !important;
        color: #2F2342 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
      }
      .stButton > button:hover {
        background: linear-gradient(135deg, #A893DB, #BC9FDC) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(185,167,232,0.35) !important;
      }

      /* Secondary / SOS Link Buttons */
      .sos-link-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #F2BFD1, #E8A8C4);
        color: #392E4D !important;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 12px 24px;
        border-radius: 12px;
        border: 1px solid #E89BBB;
        box-shadow: 0 3px 12px rgba(242,191,209,0.4);
        transition: all 0.2s ease;
      }
      .sos-link-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(242,191,209,0.6);
      }

      /* Pills and Tags */
      .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(185,167,232,0.18);
        border: 1px solid #B9A7E8;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #63438E;
        font-weight: 600;
      }

      .demo-tag {
        background: #FCECF3;
        border: 1px solid #F2BFD1;
        color: #8C395B;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
      }

      /* Clean Disclaimer Box */
      .clean-disclaimer {
        background: #FFFFFF;
        border-left: 4px solid #B9A7E8;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        font-size: 0.85rem;
        color: #645677;
        line-height: 1.6;
        margin: 20px 0;
        box-shadow: 0 1px 8px rgba(185,167,232,0.10);
      }

      /* Section Heading */
      .section-heading-custom {
        font-size: 1.25rem;
        font-weight: 700;
        color: #392E4D;
        margin: 24px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #E8DDF2;
        display: flex;
        align-items: center;
        gap: 10px;
      }

      /* Form inputs styling */
      .stTextInput > div > div > input,
      .stSelectbox > div > div,
      .stMultiSelect > div > div {
        border-radius: 10px !important;
        border-color: #E8DDF2 !important;
      }

      /* Streamlit alert overrides */
      div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border-width: 1px !important;
      }
    </style>
    """
