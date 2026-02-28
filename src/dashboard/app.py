"""
PocketQuant Risk Intelligence Platform
Enterprise-Grade Financial Analytics Dashboard
Version 3.0 - Production Ready

A sophisticated FinTech dashboard for liquidity risk assessment
designed for financial analysts and decision-makers.

Run with: streamlit run src/dashboard/app.py --server.port 8505
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.dashboard.api_client import get_api_client

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PocketQuant | Risk Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DESIGN SYSTEM - PROFESSIONAL FINTECH PALETTE
# Sophisticated color scheme emphasizing trust, intelligence & clarity
# ============================================================================
DESIGN = {
    # Primary Palette - Deep Teal & Slate (Trust & Stability)
    "primary": "#0D9488",           # Teal - Primary accent
    "primary_dark": "#0F766E",      # Deep teal
    "primary_light": "#5EEAD4",     # Light teal
    "primary_subtle": "#CCFBF1",    # Very light teal
    
    # Secondary - Slate Blue (Intelligence)
    "secondary": "#6366F1",         # Indigo accent
    "secondary_dark": "#4F46E5",    # Deep indigo
    
    # Backgrounds
    "bg_primary": "#FAFBFC",        # Off-white main bg
    "bg_secondary": "#F1F5F9",      # Light slate
    "bg_card": "#FFFFFF",           # Pure white
    "bg_dark": "#0F172A",           # Deep navy
    "bg_elevated": "#F8FAFC",       # Elevated surface
    
    # Text
    "text_primary": "#0F172A",      # Near black
    "text_secondary": "#475569",    # Slate
    "text_tertiary": "#94A3B8",     # Light slate
    "text_inverse": "#F8FAFC",      # White
    
    # Semantic Colors
    "success": "#059669",           # Emerald
    "success_bg": "#ECFDF5",        # Light emerald
    "warning": "#D97706",           # Amber
    "warning_bg": "#FFFBEB",        # Light amber
    "danger": "#DC2626",            # Red
    "danger_bg": "#FEF2F2",         # Light red
    "info": "#0284C7",              # Sky
    "info_bg": "#F0F9FF",           # Light sky
    
    # Charts
    "chart_primary": "#0D9488",     # Teal
    "chart_secondary": "#6366F1",   # Indigo
    "chart_positive": "#10B981",    # Green
    "chart_negative": "#EF4444",    # Red
    "chart_neutral": "#64748B",     # Slate
    
    # Borders
    "border_light": "#E2E8F0",
    "border_dark": "#CBD5E1",
}

RISK_LEVELS = {
    "minimal": {"color": "#059669", "bg": "#ECFDF5", "label": "MINIMAL", "desc": "Excellent financial health"},
    "low": {"color": "#10B981", "bg": "#D1FAE5", "label": "LOW", "desc": "Healthy liquidity position"},
    "moderate": {"color": "#D97706", "bg": "#FEF3C7", "label": "MODERATE", "desc": "Monitor closely"},
    "high": {"color": "#EA580C", "bg": "#FFEDD5", "label": "HIGH", "desc": "Action recommended"},
    "critical": {"color": "#DC2626", "bg": "#FEF2F2", "label": "CRITICAL", "desc": "Immediate attention required"},
}

# ============================================================================
# ENTERPRISE CSS STYLING
# ============================================================================
st.markdown("""
<style>
/* =========================================================================
   TYPOGRAPHY & FONTS
   ========================================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

:root {
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-display: 'DM Sans', 'Inter', sans-serif;
    --primary: #0D9488;
    --primary-dark: #0F766E;
    --bg-main: #FAFBFC;
    --bg-card: #FFFFFF;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --border: #E2E8F0;
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-xl: 20px;
}

* { font-family: var(--font-sans); }
code, .mono { font-family: var(--font-sans); }

/* =========================================================================
   HIDE STREAMLIT DEFAULTS
   ========================================================================= */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"], 
[data-testid="collapsedControl"] { display: none !important; }

/* =========================================================================
   MAIN CONTAINER
   ========================================================================= */
.stApp {
    background: linear-gradient(180deg, #FAFBFC 0%, #F1F5F9 100%);
}

.main .block-container {
    padding: 2rem 3rem 2.5rem;
    max-width: 1480px;
}

/* Global column gap for all Streamlit columns */
[data-testid="stHorizontalBlock"] {
    gap: 1.2rem !important;
}

/* Extra vertical breathing room between stacked elements */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"] > div:not(:first-child) {
    margin-top: 4px;
}

/* =========================================================================
   TOP NAVIGATION BAR
   ========================================================================= */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 32px;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border-radius: var(--radius-xl);
    margin-bottom: 28px;
    box-shadow: var(--shadow-lg), 0 0 0 1px rgba(255,255,255,0.05) inset;
    min-height: 90px;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 16px;
}

.nav-logo {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 2px 8px rgba(13, 148, 136, 0.35);
}

.nav-title {
    font-size: 24px;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}

.nav-subtitle {
    font-size: 11px;
    color: #64748B;
    letter-spacing: 0.12em;
    font-weight: 600;
    text-transform: uppercase;
    margin-top: 3px;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 20px;
}

.nav-stat {
    text-align: right;
}

.nav-stat-label {
    font-size: 9px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

.nav-stat-value {
    font-size: 13px;
    color: #F8FAFC;
    font-weight: 600;
    font-family: var(--font-display);
    margin-top: 1px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
}

.status-online {
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.status-offline {
    background: rgba(239, 68, 68, 0.12);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* =========================================================================
   MERCHANT CONTEXT BAR (replaces old control panel)
   ========================================================================= */
.merchant-context-bar {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 18px 28px;
    margin-bottom: 8px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
}

.merchant-meta-inline {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}

.merchant-meta-inline .meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    background: var(--bg-secondary);
    border-radius: 100px;
    font-size: 11px;
    font-weight: 500;
    color: var(--text-secondary);
    border: 1px solid var(--border);
}

.merchant-context-name {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.merchant-context-id {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    margin-left: 6px;
    letter-spacing: 0.02em;
}

.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* =========================================================================
   KPI CARDS
   ========================================================================= */
.kpi-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 24px 26px;
    border: 1px solid var(--border);
    position: relative;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-xs);
    overflow: hidden;
    margin-bottom: 6px;
}

.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
    opacity: 0;
    transition: opacity 0.2s;
}

.kpi-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--primary);
}

.kpi-card:hover::after {
    opacity: 1;
}

.kpi-icon {
    position: absolute;
    top: 18px;
    right: 18px;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    border: 1px solid rgba(13, 148, 136, 0.15);
    box-shadow: 0 2px 6px rgba(13, 148, 136, 0.12);
}

.kpi-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    font-family: var(--font-display);
    line-height: 1;
    letter-spacing: -0.02em;
}

.kpi-trend {
    font-size: 11px;
    font-weight: 600;
    margin-top: 12px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 100px;
}

.trend-up { color: #059669; background: rgba(5, 150, 105, 0.10); border: 1px solid rgba(5, 150, 105, 0.15); }
.trend-down { color: #DC2626; background: rgba(220, 38, 38, 0.08); border: 1px solid rgba(220, 38, 38, 0.12); }
.trend-neutral { color: var(--text-muted); background: var(--bg-secondary); border: 1px solid var(--border); }

/* =========================================================================
   RISK SCORE PANEL
   ========================================================================= */
.risk-panel {
    background: linear-gradient(145deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    border-radius: var(--radius-lg);
    padding: 32px 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(15, 23, 42, 0.25);
    margin-bottom: 6px;
}

.risk-panel::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(13, 148, 136, 0.18) 0%, transparent 70%);
    pointer-events: none;
}

.risk-panel::after {
    content: '';
    position: absolute;
    bottom: -50px;
    left: -50px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, transparent 70%);
    pointer-events: none;
}

.risk-content {
    position: relative;
    z-index: 1;
    text-align: center;
}

.risk-label {
    font-size: 10px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 16px;
}

.risk-score {
    font-size: 80px;
    font-weight: 800;
    font-family: var(--font-display);
    line-height: 1;
    margin-bottom: 10px;
    text-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    letter-spacing: -0.02em;
}

.risk-level-text {
    font-size: 15px;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}

.risk-threshold-info {
    font-size: 11px;
    color: #64748B;
    font-weight: 500;
}

.risk-bar-bg {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 100px;
    height: 5px;
    margin-top: 22px;
    overflow: hidden;
}

.risk-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 12px rgba(var(--fill-rgb, 0,0,0), 0.4);
}

/* Risk Stats Row (inside dark panel) */
.risk-stats-row {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.risk-stat-item {
    text-align: center;
}

.risk-stat-val {
    font-size: 16px;
    font-weight: 700;
    color: #E2E8F0;
    font-family: var(--font-display);
    line-height: 1;
}

.risk-stat-lbl {
    font-size: 9px;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

/* Right-side assessment card */
.assessment-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    height: 100%;
}

.assessment-header {
    padding: 18px 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.assessment-header-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.assessment-body {
    padding: 20px 24px;
}

.assessment-metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 16px;
}

.assessment-metric {
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    border: 1px solid var(--border);
}

.assessment-metric-label {
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}

.assessment-metric-value {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    font-family: var(--font-display);
    line-height: 1;
}

/* =========================================================================
   ALERT PANELS
   ========================================================================= */
.alert {
    border-radius: var(--radius-lg);
    padding: 18px 22px;
    margin-bottom: 12px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
    transition: box-shadow 0.15s;
}

.alert:hover {
    box-shadow: var(--shadow-sm);
}

.alert-success { 
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border-left: 4px solid #059669;
}
.alert-warning { 
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-left: 4px solid #D97706;
}
.alert-danger { 
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border-left: 4px solid #DC2626;
}
.alert-info { 
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
    border-left: 4px solid #0284C7;
}

.alert-icon {
    font-size: 20px;
    line-height: 1;
    flex-shrink: 0;
    margin-top: 1px;
}

.alert-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}

.alert-text {
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* =========================================================================
   RISK FACTORS
   ========================================================================= */
.factors-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.factor-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    color: #991B1B;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid rgba(220, 38, 38, 0.18);
    transition: all 0.2s;
    box-shadow: 0 1px 2px rgba(220, 38, 38, 0.06);
    letter-spacing: 0.01em;
}

.factor-chip:hover {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(220, 38, 38, 0.12);
}

/* =========================================================================
   SECTION HEADERS
   ========================================================================= */
.section-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-dark);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 36px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 48px;
    height: 2px;
    background: var(--primary);
    border-radius: 2px;
}

/* =========================================================================
   CHART CARDS
   ========================================================================= */
.chart-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 26px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
    margin-bottom: 6px;
}

.chart-card:hover {
    box-shadow: var(--shadow-md);
}

.chart-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
    padding: 20px 24px 0;
}

/* Chart wrapper applied via stColumn containers */
[data-testid="stVerticalBlock"] .chart-title + div {
    padding: 0 12px 12px;
}

/* =========================================================================
   TABS
   ========================================================================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--bg-secondary);
    padding: 4px;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: var(--radius-md);
    padding: 10px 22px;
    font-weight: 600;
    font-size: 12px;
    color: var(--text-secondary);
    border: none;
    transition: all 0.15s;
    letter-spacing: 0.01em;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(255,255,255,0.5);
}

.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--primary-dark) !important;
    box-shadow: var(--shadow-sm);
    font-weight: 700;
}

/* =========================================================================
   DETAIL CARDS
   ========================================================================= */
.detail-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 24px 20px;
    text-align: center;
    border: 1px solid var(--border);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-xs);
    position: relative;
    overflow: hidden;
    margin-bottom: 6px;
}

.detail-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
    opacity: 0;
    transition: opacity 0.2s;
}

.detail-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--primary);
}

.detail-card:hover::after {
    opacity: 1;
}

.detail-status {
    font-size: 18px;
    margin-bottom: 10px;
    width: 36px;
    height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
}

.detail-status-healthy {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    color: #059669;
    border: 1px solid rgba(5, 150, 105, 0.15);
}

.detail-status-warning {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    color: #DC2626;
    border: 1px solid rgba(220, 38, 38, 0.15);
}

.detail-status-info {
    background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
    color: #0D9488;
    border: 1px solid rgba(13, 148, 136, 0.15);
}

.detail-value {
    font-size: 24px;
    font-weight: 800;
    color: var(--text-primary);
    font-family: var(--font-display);
    margin-bottom: 6px;
    letter-spacing: -0.02em;
}

.detail-label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* =========================================================================
   FOOTER
   ========================================================================= */
.footer {
    text-align: center;
    padding: 36px 0 16px;
    margin-top: 48px;
    border-top: 2px solid var(--border);
    position: relative;
}

.footer::before {
    content: '';
    position: absolute;
    top: -2px;
    left: 50%;
    transform: translateX(-50%);
    width: 48px;
    height: 2px;
    background: var(--primary);
}

.footer-text {
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.8;
    font-weight: 500;
}

/* =========================================================================
   SELECTBOX & MULTISELECT OVERRIDE
   ========================================================================= */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

/* Fix selectbox text color - make it bold and visible */
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] > div > div,
.stSelectbox input,
.stSelectbox label,
.stSelectbox p,
.stSelectbox span,
.stMultiSelect [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] span,
.stMultiSelect input {
    color: #0F172A !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* Selected value text */
.stSelectbox [data-baseweb="select"] [data-testid="stMarkdownContainer"],
.stSelectbox [data-baseweb="select"] > div:first-child {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Multiselect tags (selected items) */
.stMultiSelect [data-baseweb="tag"] {
    background: #CCFBF1 !important;
    border: 1px solid #0D9488 !important;
    border-radius: 20px !important;
    color: #0F766E !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 2px 8px !important;
}

.stMultiSelect [data-baseweb="tag"] span {
    color: #0F766E !important;
    font-weight: 600 !important;
}

.stMultiSelect [data-baseweb="tag"] svg {
    fill: #0D9488 !important;
}

/* Dropdown arrow icon */
.stSelectbox svg,
.stSelectbox [data-baseweb="select"] svg,
.stMultiSelect svg {
    fill: #0D9488 !important;
    color: #0D9488 !important;
}

/* Text input styling */
.stTextInput > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

.stTextInput > div > div:hover,
.stTextInput > div > div:focus-within {
    border-color: var(--primary) !important;
}

.stTextInput input {
    color: #0F172A !important;
    font-weight: 500 !important;
}

/* =========================================================================
   MERCHANT COMPARISON TABLE
   ========================================================================= */
.comparison-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
    margin: 8px 0 16px;
    font-family: var(--font-body);
}

.comparison-table thead th {
    background: #0F172A;
    color: #F8FAFC;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 12px 14px;
    text-align: left;
    white-space: nowrap;
    border-bottom: 2px solid #0D9488;
}

.comparison-table thead th:first-child {
    border-left: 1px solid #E2E8F0;
}

.comparison-table tbody tr {
    transition: background 0.15s;
    cursor: pointer;
}

.comparison-table tbody tr:nth-child(even) {
    background: #F8FAFC;
}

.comparison-table tbody tr:hover {
    background: #CCFBF1;
}

.comparison-table tbody tr.active-row {
    background: #CCFBF1;
    border-left: 3px solid #0D9488;
}

.comparison-table td {
    padding: 10px 14px;
    font-size: 12px;
    color: #0F172A;
    border-bottom: 1px solid #F1F5F9;
    font-weight: 500;
}

.comparison-table td:first-child {
    font-weight: 700;
    border-left: 1px solid #E2E8F0;
}

.comparison-table td:last-child,
.comparison-table th:last-child {
    border-right: 1px solid #E2E8F0;
}

.comparison-table tbody tr:last-child td {
    border-bottom: 2px solid #E2E8F0;
}

.table-risk-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.filter-bar {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.filter-label {
    font-size: 10px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}

/* ===== DROPDOWN MENU STYLING ===== */
/* Dropdown menu container */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="select"] [data-baseweb="popover"],
ul[role="listbox"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
}

/* Dropdown menu items */
[data-baseweb="menu"] li,
[data-baseweb="popover"] li,
[role="option"],
li[data-baseweb="menu-item"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
}

/* Dropdown menu item text */
[data-baseweb="menu"] li span,
[data-baseweb="popover"] li span,
[role="option"] span,
li[data-baseweb="menu-item"] span {
    color: #0F172A !important;
    font-weight: 500 !important;
}

/* Dropdown menu item hover */
[data-baseweb="menu"] li:hover,
[data-baseweb="popover"] li:hover,
[role="option"]:hover,
li[data-baseweb="menu-item"]:hover {
    background: #F1F5F9 !important;
    color: #0D9488 !important;
}

/* Highlighted/focused item */
[data-baseweb="menu"] li[aria-selected="true"],
[data-baseweb="popover"] li[aria-selected="true"],
[role="option"][aria-selected="true"],
li[data-baseweb="menu-item"][aria-selected="true"] {
    background: #CCFBF1 !important;
    color: #0F766E !important;
}

[data-baseweb="menu"] li[aria-selected="true"] span,
[role="option"][aria-selected="true"] span {
    color: #0F766E !important;
    font-weight: 600 !important;
}

/* =========================================================================
   SLIDER OVERRIDE
   ========================================================================= */
.stSlider > div > div > div {
    background: var(--border) !important;
}

.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #0D9488 0%, #0F766E 100%) !important;
}

.stSlider > div > div > div > div > div {
    background: var(--primary) !important;
    box-shadow: 0 2px 6px rgba(13, 148, 136, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# MERCHANT DATA GENERATOR — 120 diverse merchants
# ============================================================================

_MERCHANT_PROFILES = [
    # (name, category, sub_category, city, state)
    ("RetailMart", "Retail", "Supermarket", "Mumbai", "Maharashtra"),
    ("FoodZone", "Food & Beverage", "Restaurant", "Delhi", "Delhi"),
    ("QuickMeds", "Healthcare", "Pharmacy", "Pune", "Maharashtra"),
    ("GroceryKing", "Grocery", "Supermarket", "Surat", "Gujarat"),
    ("TechHub", "Electronics", "Mobile Store", "Bengaluru", "Karnataka"),
    ("FashionVilla", "Fashion", "Clothing", "Mumbai", "Maharashtra"),
    ("AutoParts Plus", "Automotive", "Spare Parts", "Chennai", "Tamil Nadu"),
    ("BookWorld", "Education", "Bookstore", "Kolkata", "West Bengal"),
    ("FitLife Gym", "Health & Fitness", "Gym", "Hyderabad", "Telangana"),
    ("CafeBliss", "Food & Beverage", "Cafe", "Bengaluru", "Karnataka"),
    ("GreenGrocer", "Grocery", "Organic Store", "Jaipur", "Rajasthan"),
    ("PetCare Hub", "Pet Services", "Pet Store", "Pune", "Maharashtra"),
    ("SparkElectric", "Electronics", "Appliances", "Ahmedabad", "Gujarat"),
    ("StyleCraft", "Fashion", "Boutique", "Delhi", "Delhi"),
    ("MedPlus", "Healthcare", "Clinic", "Hyderabad", "Telangana"),
    ("QuickBite", "Food & Beverage", "Fast Food", "Chennai", "Tamil Nadu"),
    ("HomeDecor", "Home & Living", "Furniture", "Lucknow", "Uttar Pradesh"),
    ("GadgetWorld", "Electronics", "Gadgets", "Noida", "Uttar Pradesh"),
    ("FreshMart", "Grocery", "Fresh Produce", "Mumbai", "Maharashtra"),
    ("WellnessFirst", "Healthcare", "Wellness Center", "Bengaluru", "Karnataka"),
    ("UrbanWear", "Fashion", "Streetwear", "Pune", "Maharashtra"),
    ("ToolStation", "Hardware", "Tools & Equipment", "Nagpur", "Maharashtra"),
    ("EduSmart", "Education", "Coaching Center", "Kota", "Rajasthan"),
    ("JewelCraft", "Jewelry", "Gold & Diamond", "Jaipur", "Rajasthan"),
    ("SportsArena", "Sports", "Equipment", "Delhi", "Delhi"),
    ("BabyBloom", "Retail", "Baby Products", "Gurgaon", "Haryana"),
    ("TravelEase", "Travel", "Travel Agency", "Goa", "Goa"),
    ("PrintExpress", "Services", "Printing", "Chennai", "Tamil Nadu"),
    ("FlowerBay", "Retail", "Florist", "Chandigarh", "Punjab"),
    ("KidZone", "Retail", "Toy Store", "Indore", "Madhya Pradesh"),
    ("CyclePro", "Sports", "Bicycle Shop", "Pune", "Maharashtra"),
    ("MeatFresh", "Grocery", "Meat & Seafood", "Kochi", "Kerala"),
    ("OpticalPlus", "Healthcare", "Eye Care", "Ahmedabad", "Gujarat"),
    ("SalonElite", "Beauty", "Salon", "Mumbai", "Maharashtra"),
    ("OfficeHub", "Services", "Stationery", "Bengaluru", "Karnataka"),
    ("SweetTreats", "Food & Beverage", "Bakery", "Lucknow", "Uttar Pradesh"),
    ("PhoneRepair", "Services", "Mobile Repair", "Hyderabad", "Telangana"),
    ("AquaPure", "Retail", "Water Purifier", "Delhi", "Delhi"),
    ("VegDelight", "Food & Beverage", "Vegetarian", "Ahmedabad", "Gujarat"),
    ("TimePiece", "Jewelry", "Watches", "Surat", "Gujarat"),
    ("PhotoStudio", "Services", "Photography", "Kolkata", "West Bengal"),
    ("YogaBliss", "Health & Fitness", "Yoga Studio", "Rishikesh", "Uttarakhand"),
    ("LaundryExpress", "Services", "Laundry", "Noida", "Uttar Pradesh"),
    ("CakeFactory", "Food & Beverage", "Cake Shop", "Pune", "Maharashtra"),
    ("GardenCenter", "Home & Living", "Nursery", "Coimbatore", "Tamil Nadu"),
    ("MusicWorld", "Entertainment", "Music Store", "Mumbai", "Maharashtra"),
    ("SpiceTrail", "Grocery", "Spice Store", "Kochi", "Kerala"),
    ("DentalCare", "Healthcare", "Dental Clinic", "Bengaluru", "Karnataka"),
    ("ShoeLocker", "Fashion", "Footwear", "Chennai", "Tamil Nadu"),
    ("TireMaster", "Automotive", "Tire Shop", "Nagpur", "Maharashtra"),
    ("CloudKitchen", "Food & Beverage", "Cloud Kitchen", "Gurgaon", "Haryana"),
    ("PaintPro", "Hardware", "Paint Store", "Jaipur", "Rajasthan"),
    ("SmartHome", "Electronics", "Smart Devices", "Bengaluru", "Karnataka"),
    ("OrganicBasket", "Grocery", "Organic", "Mysuru", "Karnataka"),
    ("DigiPrint", "Services", "Digital Printing", "Delhi", "Delhi"),
    ("LuxeWatch", "Jewelry", "Luxury Watches", "Mumbai", "Maharashtra"),
    ("GymGear", "Sports", "Gym Equipment", "Hyderabad", "Telangana"),
    ("BridalHouse", "Fashion", "Bridal Wear", "Lucknow", "Uttar Pradesh"),
    ("PharmaLife", "Healthcare", "Pharmacy", "Patna", "Bihar"),
    ("NoodleBar", "Food & Beverage", "Chinese", "Kolkata", "West Bengal"),
    ("FurniCraft", "Home & Living", "Custom Furniture", "Jodhpur", "Rajasthan"),
    ("ElectroFix", "Services", "Electronics Repair", "Chennai", "Tamil Nadu"),
    ("GreenLeaf", "Grocery", "Vegetables", "Nashik", "Maharashtra"),
    ("VetCare", "Pet Services", "Veterinary", "Pune", "Maharashtra"),
    ("ArtGallery", "Entertainment", "Art Store", "Jaipur", "Rajasthan"),
    ("KidsAcademy", "Education", "Preschool", "Gurgaon", "Haryana"),
    ("MilkBasket", "Grocery", "Dairy", "Noida", "Uttar Pradesh"),
    ("SkinGlow", "Beauty", "Skincare", "Mumbai", "Maharashtra"),
    ("BikeZone", "Automotive", "Two Wheeler", "Pune", "Maharashtra"),
    ("ChaiPoint", "Food & Beverage", "Tea House", "Bengaluru", "Karnataka"),
    ("CeramicArt", "Home & Living", "Pottery", "Khurja", "Uttar Pradesh"),
    ("NetSpeed", "Services", "Internet Cafe", "Varanasi", "Uttar Pradesh"),
    ("Trophy House", "Retail", "Awards & Gifts", "Delhi", "Delhi"),
    ("FrameIt", "Services", "Frame Making", "Ahmedabad", "Gujarat"),
    ("IceCreamParl", "Food & Beverage", "Ice Cream", "Indore", "Madhya Pradesh"),
    ("SolarEnergy", "Electronics", "Solar Panels", "Jodhpur", "Rajasthan"),
    ("HerbShop", "Healthcare", "Ayurvedic", "Haridwar", "Uttarakhand"),
    ("DanceStudio", "Entertainment", "Dance Academy", "Mumbai", "Maharashtra"),
    ("CopierWorld", "Services", "Office Equipment", "Delhi", "Delhi"),
    ("FishMarket", "Grocery", "Seafood", "Visakhapatnam", "Andhra Pradesh"),
    ("TailorMade", "Fashion", "Tailor Shop", "Ludhiana", "Punjab"),
    ("SteelMart", "Hardware", "Steel & Iron", "Raipur", "Chhattisgarh"),
    ("Aromatherapy", "Beauty", "Spa", "Goa", "Goa"),
    ("PizzaCorner", "Food & Beverage", "Pizza", "Hyderabad", "Telangana"),
    ("LaptopClinic", "Services", "Laptop Repair", "Bengaluru", "Karnataka"),
    ("DryCleaner", "Services", "Dry Cleaning", "Chandigarh", "Punjab"),
    ("JuiceBar", "Food & Beverage", "Juice Bar", "Surat", "Gujarat"),
    ("CarpetKing", "Home & Living", "Carpets", "Agra", "Uttar Pradesh"),
    ("EyeWear", "Fashion", "Sunglasses", "Mumbai", "Maharashtra"),
    ("Diagnostics+", "Healthcare", "Diagnostic Lab", "Delhi", "Delhi"),
    ("GameZone", "Entertainment", "Gaming Arcade", "Pune", "Maharashtra"),
    ("FuelMart", "Automotive", "Fuel Station", "Chennai", "Tamil Nadu"),
    ("NutriStore", "Healthcare", "Nutrition", "Bengaluru", "Karnataka"),
    ("PackShip", "Services", "Packaging", "Ahmedabad", "Gujarat"),
    ("SilkEmporium", "Fashion", "Silk & Saree", "Varanasi", "Uttar Pradesh"),
    ("BatteryWorld", "Automotive", "Battery Shop", "Nagpur", "Maharashtra"),
    ("SnackHouse", "Food & Beverage", "Snacks", "Indore", "Madhya Pradesh"),
    ("PlumbFix", "Services", "Plumbing", "Jaipur", "Rajasthan"),
    ("RiceTrader", "Grocery", "Rice & Grains", "Thanjavur", "Tamil Nadu"),
    ("LightHouse", "Electronics", "Lighting", "Surat", "Gujarat"),
    ("NailStudio", "Beauty", "Nail Art", "Mumbai", "Maharashtra"),
    ("WoodWorks", "Home & Living", "Woodcraft", "Saharanpur", "Uttar Pradesh"),
    ("PureGold", "Jewelry", "Gold", "Thrissur", "Kerala"),
    ("FarmFresh", "Grocery", "Farm Products", "Nashik", "Maharashtra"),
    ("TutorHub", "Education", "Tutoring", "Delhi", "Delhi"),
    ("BiryaniHouse", "Food & Beverage", "Biryani", "Hyderabad", "Telangana"),
    ("MotorCare", "Automotive", "Car Service", "Bengaluru", "Karnataka"),
    ("PaperMill", "Services", "Paper Products", "Lucknow", "Uttar Pradesh"),
    ("SugarNCream", "Food & Beverage", "Desserts", "Kolkata", "West Bengal"),
    ("DigiStore", "Electronics", "Accessories", "Ahmedabad", "Gujarat"),
    ("MedEquip", "Healthcare", "Medical Equipment", "Chennai", "Tamil Nadu"),
    ("FlexiPack", "Services", "Flex Printing", "Rajkot", "Gujarat"),
    ("KeralaSpice", "Grocery", "Spices & Herbs", "Kozhikode", "Kerala"),
    ("StyleStudio", "Beauty", "Hair Salon", "Pune", "Maharashtra"),
    ("SafeLocker", "Services", "Safety Equipment", "Delhi", "Delhi"),
    ("EcoMart", "Grocery", "Eco Products", "Bengaluru", "Karnataka"),
    ("CoolBreeze", "Electronics", "AC & Coolers", "Jodhpur", "Rajasthan"),
    ("PanMasala", "Retail", "FMCG", "Kanpur", "Uttar Pradesh"),
    ("GlassHouse", "Home & Living", "Glassware", "Firozabad", "Uttar Pradesh"),
]

_KYC_STATUSES = ["Verified", "Verified", "Verified", "Verified", "Pending", "Under Review"]

def _generate_all_merchants() -> dict:
    """Generate 120 realistic merchants with varied financial profiles."""
    rng = np.random.RandomState(2026)
    merchants = {}
    
    for i, (name, cat, sub_cat, city, state) in enumerate(_MERCHANT_PROFILES):
        mid = f"M{i+1:03d}"
        key = f"{mid} - {name}"
        
        # Financial profile archetype (healthy → stressed)
        archetype = rng.choice(["healthy", "stable", "moderate", "stressed", "critical"],
                               p=[0.20, 0.25, 0.25, 0.20, 0.10])
        
        if archetype == "healthy":
            daily_inflow = rng.uniform(20000, 80000)
            io_ratio = rng.uniform(1.2, 1.8)
            credit_util = rng.uniform(0.05, 0.30)
            buffer_days = rng.uniform(7, 15)
            volatility = rng.uniform(0.03, 0.12)
            stress = rng.uniform(0.02, 0.15)
            revenue_decline = rng.uniform(0.0, 0.05)
            consec_drop = 0
            risk_seg = "Low"
        elif archetype == "stable":
            daily_inflow = rng.uniform(12000, 45000)
            io_ratio = rng.uniform(1.05, 1.30)
            credit_util = rng.uniform(0.20, 0.50)
            buffer_days = rng.uniform(4, 8)
            volatility = rng.uniform(0.08, 0.20)
            stress = rng.uniform(0.10, 0.30)
            revenue_decline = rng.uniform(-0.05, 0.03)
            consec_drop = rng.choice([0, 0, 1])
            risk_seg = "Low"
        elif archetype == "moderate":
            daily_inflow = rng.uniform(8000, 30000)
            io_ratio = rng.uniform(0.90, 1.15)
            credit_util = rng.uniform(0.40, 0.65)
            buffer_days = rng.uniform(2.5, 5)
            volatility = rng.uniform(0.15, 0.35)
            stress = rng.uniform(0.25, 0.50)
            revenue_decline = rng.uniform(-0.12, -0.02)
            consec_drop = rng.choice([0, 1, 2, 3])
            risk_seg = "Medium"
        elif archetype == "stressed":
            daily_inflow = rng.uniform(4000, 15000)
            io_ratio = rng.uniform(0.65, 0.95)
            credit_util = rng.uniform(0.60, 0.85)
            buffer_days = rng.uniform(1, 3)
            volatility = rng.uniform(0.30, 0.55)
            stress = rng.uniform(0.50, 0.75)
            revenue_decline = rng.uniform(-0.25, -0.10)
            consec_drop = rng.choice([2, 3, 4, 5])
            risk_seg = "High"
        else:  # critical
            daily_inflow = rng.uniform(2000, 8000)
            io_ratio = rng.uniform(0.35, 0.70)
            credit_util = rng.uniform(0.80, 0.98)
            buffer_days = rng.uniform(0.3, 1.5)
            volatility = rng.uniform(0.45, 0.75)
            stress = rng.uniform(0.70, 0.95)
            revenue_decline = rng.uniform(-0.40, -0.20)
            consec_drop = rng.choice([4, 5, 6, 7])
            risk_seg = "Critical"
        
        daily_outflow = daily_inflow / io_ratio
        net_cf = daily_inflow - daily_outflow
        txn_count = int(rng.uniform(10, 200))
        buffer_ratio = buffer_days * rng.uniform(0.6, 0.9)
        coverage = io_ratio * rng.uniform(0.7, 1.2)
        wc_indicator = (io_ratio - 1) * rng.uniform(0.8, 1.5)
        debt_service = credit_util * rng.uniform(0.5, 0.9)
        
        r3d = daily_inflow * rng.uniform(0.95, 1.05)
        r7d = daily_inflow * rng.uniform(0.92, 1.08)
        r14d = daily_inflow * rng.uniform(0.88, 1.12)
        r7d_out = daily_outflow * rng.uniform(0.95, 1.05)
        r7d_net = r7d - r7d_out
        
        stress_intensity = stress * rng.uniform(0.80, 1.0)
        vol_norm = volatility * rng.uniform(0.85, 1.15)
        rev_drop_7d = 1.0 if revenue_decline < -0.10 else 0.0
        rev_sig = 1 if revenue_decline < -0.15 else 0
        rev_severe = 1 if revenue_decline < -0.25 else 0
        
        kyc = rng.choice(_KYC_STATUSES)
        
        merchants[key] = {
            "daily_inflow": round(daily_inflow, 2),
            "daily_outflow_estimated": round(daily_outflow, 2),
            "net_cash_flow": round(net_cf, 2),
            "transaction_count": txn_count,
            "inflow_outflow_ratio": round(io_ratio, 2),
            "credit_utilization_ratio": round(credit_util, 2),
            "liquidity_buffer_days": round(buffer_days, 1),
            "liquidity_buffer_ratio": round(buffer_ratio, 2),
            "cashflow_coverage_ratio": round(coverage, 2),
            "working_capital_indicator": round(wc_indicator, 2),
            "debt_service_ratio": round(debt_service, 2),
            "rolling_3d_inflow": round(r3d, 2),
            "rolling_7d_inflow": round(r7d, 2),
            "rolling_14d_inflow": round(r14d, 2),
            "rolling_7d_outflow": round(r7d_out, 2),
            "rolling_7d_net_cashflow": round(r7d_net, 2),
            "rolling_7d_inflow_cv": round(volatility * rng.uniform(0.8, 1.2), 2),
            "rolling_7d_volatility": round(volatility, 2),
            "stress_score_composite": round(stress, 2),
            "stress_intensity_score": round(stress_intensity, 2),
            "volatility_score_normalized": round(vol_norm, 2),
            "revenue_decline_pct": round(revenue_decline, 2),
            "consecutive_drop_days": int(consec_drop),
            "revenue_drop_7d": rev_drop_7d,
            "revenue_drop_significant": rev_sig,
            "revenue_drop_severe": rev_severe,
            "credit_vol_interaction": round(credit_util * volatility, 2),
            "stress_buffer_interaction": round(stress * buffer_days * 0.15, 2),
            "revdrop_credit_interaction": round(revenue_decline * credit_util, 3),
            "gap_volatility_interaction": round((1 - io_ratio) * volatility, 2) if io_ratio < 1 else round(0.01, 2),
            "month": 2,
            "is_weekend": 0,
            "merchant_category": cat,
            "merchant_sub_category": sub_cat,
            "merchant_city": city,
            "merchant_state": state,
            "kyc_status": kyc,
            "risk_segment_internal": risk_seg,
        }
    
    return merchants

SAMPLE_MERCHANTS = _generate_all_merchants()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_risk_level_config(probability: float) -> dict:
    """Get risk configuration based on probability."""
    if probability >= 0.8:
        return RISK_LEVELS["critical"]
    elif probability >= 0.6:
        return RISK_LEVELS["high"]
    elif probability >= 0.4:
        return RISK_LEVELS["moderate"]
    elif probability >= 0.2:
        return RISK_LEVELS["low"]
    else:
        return RISK_LEVELS["minimal"]


def create_cashflow_chart(data: pd.DataFrame) -> go.Figure:
    """Create professional cash flow chart."""
    fig = go.Figure()
    
    # Inflow bars
    fig.add_trace(go.Bar(
        name='Inflow',
        x=data['date'],
        y=data['inflow'],
        marker=dict(
            color='#10B981',
            cornerradius=4,
            line=dict(width=0)
        ),
        hovertemplate='<b>Inflow</b><br>₹%{y:,.0f}<extra></extra>'
    ))
    
    # Outflow bars
    fig.add_trace(go.Bar(
        name='Outflow',
        x=data['date'],
        y=data['outflow'],
        marker=dict(
            color='#EF4444',
            cornerradius=4,
            line=dict(width=0)
        ),
        hovertemplate='<b>Outflow</b><br>₹%{y:,.0f}<extra></extra>'
    ))
    
    # Net flow line
    fig.add_trace(go.Scatter(
        name='Net Flow',
        x=data['date'],
        y=data['net'],
        mode='lines+markers',
        line=dict(color='#0D9488', width=2.5, shape='spline'),
        marker=dict(size=7, color='#0D9488', line=dict(width=2, color='white')),
        hovertemplate='<b>Net</b><br>₹%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='group',
        bargap=0.2,
        bargroupgap=0.1,
        height=280,
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#475569', size=10),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='#E2E8F0',
            linewidth=1,
            tickfont=dict(size=10, color='#64748B')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F1F5F9',
            gridwidth=1,
            showline=False,
            tickfont=dict(size=10, color='#64748B'),
            tickprefix='₹',
            tickformat=',.0f'
        ),
        hovermode='x unified'
    )
    
    return fig


def create_radar_chart(data: dict) -> go.Figure:
    """Create financial health radar chart."""
    categories = ['Liquidity', 'Credit', 'Cash Flow', 'Stability', 'Growth']
    values = [
        min(100, data.get('liquidity_buffer_ratio', 5) * 15),
        max(0, 100 - data.get('credit_utilization_ratio', 0.5) * 100),
        min(100, max(0, (data.get('inflow_outflow_ratio', 1) - 0.5) * 100)),
        max(0, 100 - data.get('rolling_7d_volatility', 0.3) * 200),
        max(0, 50 + data.get('revenue_decline_pct', 0) * 200)
    ]
    values.append(values[0])
    categories.append(categories[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(13, 148, 136, 0.12)',
        line=dict(color='#0D9488', width=2),
        marker=dict(size=5, color='#0D9488'),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='#E2E8F0',
                linecolor='#E2E8F0'
            ),
            angularaxis=dict(
                gridcolor='#E2E8F0',
                linecolor='#E2E8F0',
                tickfont=dict(size=10, color='#64748B')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        margin=dict(l=50, r=50, t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter'),
        height=260
    )
    
    return fig


def generate_cashflow_data(inflow: float, outflow: float, volatility: float = 0.15) -> pd.DataFrame:
    """Generate sample cash flow data."""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=7, freq='D')
    np.random.seed(42)
    inflows = inflow * (1 + np.random.normal(0, volatility, 7))
    outflows = outflow * (1 + np.random.normal(0, volatility, 7))
    
    return pd.DataFrame({
        'date': dates.strftime('%b %d'),
        'inflow': inflows,
        'outflow': outflows,
        'net': inflows - outflows
    })


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main dashboard entry point."""
    
    # Initialize API
    api_client = get_api_client()
    health = api_client.health_check()
    api_online = health.get("status") == "healthy"
    
    current_time = datetime.now()
    time_str = current_time.strftime('%H:%M:%S')
    date_str = current_time.strftime('%b %d, %Y')
    
    # =========================================================================
    # TOP NAVIGATION BAR
    # =========================================================================
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-brand">
            <div class="nav-logo">◈</div>
            <div>
                <div class="nav-title">PocketQuant</div>
                <div class="nav-subtitle">Risk Intelligence Platform</div>
            </div>
        </div>
        <div class="nav-actions">
            <div class="nav-stat">
                <div class="nav-stat-label">Last Sync</div>
                <div class="nav-stat-value">{time_str}</div>
            </div>
            <div class="nav-stat">
                <div class="nav-stat-label">Date</div>
                <div class="nav-stat-value">{date_str}</div>
            </div>
            <div class="status-pill {'status-online' if api_online else 'status-offline'}">
                <div class="status-dot" style="background: {'#34D399' if api_online else '#F87171'};"></div>
                {'System Online' if api_online else 'Offline'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # MERCHANT MULTI-SELECT
    # =========================================================================
    all_merchants = list(SAMPLE_MERCHANTS.keys())
    
    # Filter bar
    st.markdown('<div class="section-title">Merchant Selection</div>', unsafe_allow_html=True)
    
    # Multiselect
    selected_merchants = st.multiselect(
        "Select Merchants",
        all_merchants,
        default=[all_merchants[0]],
        label_visibility="collapsed",
        placeholder="Choose one or more merchants..."
    )
    
    if not selected_merchants:
        st.warning("Please select at least one merchant to view the dashboard.")
        return
    
    # Primary merchant (first selected) drives the detailed view
    # Will be overridden below if user picks from table
    primary_merchant = selected_merchants[0]
    
    # Hidden threshold — fixed at 0.4 (removed visual slider)
    threshold = 0.4
    
    # =========================================================================
    # COMPARISON TABLE (shown when multiple merchants selected)
    # =========================================================================
    if len(selected_merchants) > 1:
        rows_html = ""
        for mk in selected_merchants:
            md = SAMPLE_MERCHANTS[mk]
            mid_t = mk.split(" - ")[0]
            mname_t = mk.split(" - ")[1]
            # quick risk estimate
            br = md.get("liquidity_buffer_ratio", 5)
            rp = 0.85 if br < 2 else 0.65 if br < 3 else 0.35 if br < 4 else 0.10
            rc = get_risk_level_config(rp)
            net_cl = "#059669" if md["net_cash_flow"] >= 0 else "#DC2626"
            rows_html += f"""
            <tr>
                <td>{mid_t}</td>
                <td>{mname_t}</td>
                <td>{md['merchant_category']}</td>
                <td>{md['merchant_city']}</td>
                <td>₹{md['daily_inflow']:,.0f}</td>
                <td style="color:{net_cl};">{'+' if md['net_cash_flow']>=0 else ''}₹{md['net_cash_flow']:,.0f}</td>
                <td>{md['liquidity_buffer_days']:.1f}</td>
                <td>{md['credit_utilization_ratio']*100:.0f}%</td>
                <td><span class="table-risk-badge" style="background:{rc['bg']};color:{rc['color']};border:1px solid {rc['color']}20;">{rc['label']}</span></td>
            </tr>"""
        
        st.markdown(f"""
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Merchant</th>
                    <th>Category</th>
                    <th>City</th>
                    <th>Daily Inflow</th>
                    <th>Net Cash Flow</th>
                    <th>Buffer Days</th>
                    <th>Credit Util.</th>
                    <th>Risk Level</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)
        
        # Merchant switcher — styled bar with selector
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 12px; padding: 14px 24px; margin: 12px 0 8px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.15);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">📊</span>
                <span style="font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">View Analysis For</span>
            </div>
            <div style="width: 1px; height: 24px; background: rgba(255,255,255,0.1);"></div>
            <span style="font-size: 11px; color: #64748B;">Select a merchant from the dropdown to switch the detailed view below</span>
        </div>
        """, unsafe_allow_html=True)
        primary_merchant = st.selectbox(
            "Switch Merchant",
            selected_merchants,
            index=0,
            label_visibility="collapsed",
            key="merchant_switcher"
        )
    
    # =========================================================================
    # GET DATA & PREDICTION
    # =========================================================================
    merchant_data = SAMPLE_MERCHANTS[primary_merchant].copy()
    merchant_id = primary_merchant.split(" - ")[0]
    merchant_name = primary_merchant.split(" - ")[1]
    
    prediction = api_client.predict_risk(merchant_data, merchant_id=merchant_id)
    
    if "error" in prediction:
        buffer_ratio = merchant_data.get("liquidity_buffer_ratio", 5)
        prob = 0.85 if buffer_ratio < 2 else 0.65 if buffer_ratio < 3 else 0.35 if buffer_ratio < 4 else 0.10
        
        prediction = {
            "risk_probability": prob,
            "risk_label": "High Risk" if prob >= threshold else "Low Risk",
            "top_risk_factors": []
        }
        
        if merchant_data.get("liquidity_buffer_ratio", 999) < 3:
            prediction["top_risk_factors"].append("Low liquidity buffer")
        if merchant_data.get("credit_utilization_ratio", 0) > 0.7:
            prediction["top_risk_factors"].append("High credit utilization")
        if merchant_data.get("rolling_7d_volatility", 0) > 0.3:
            prediction["top_risk_factors"].append("Cash flow volatility")
        if merchant_data.get("revenue_decline_pct", 0) < -0.1:
            prediction["top_risk_factors"].append("Revenue decline")
    
    risk_prob = prediction.get("risk_probability", 0)
    risk_factors = prediction.get("top_risk_factors", [])
    risk_config = get_risk_level_config(risk_prob)
    
    # =========================================================================
    # MERCHANT CONTEXT BAR
    # =========================================================================
    io_ratio = merchant_data['inflow_outflow_ratio']
    ratio_color = "#059669" if io_ratio >= 1 else "#DC2626"
    st.markdown(f"""
    <div class="merchant-context-bar">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div>
                <span class="merchant-context-name">{merchant_name}</span>
                <span class="merchant-context-id">{merchant_id}</span>
            </div>
            <div class="merchant-meta-inline">
                <span class="meta-chip">📁 {merchant_data['merchant_category']}</span>
                <span class="meta-chip">📍 {merchant_data['merchant_city']}, {merchant_data['merchant_state']}</span>
                <span class="meta-chip">✓ {merchant_data['kyc_status']}</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="text-align: center; padding: 0 12px;">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A; font-family: var(--font-display);">{merchant_data['transaction_count']}</div>
                <div style="font-size: 9px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;">Txns</div>
            </div>
            <div style="width: 1px; height: 28px; background: #E2E8F0;"></div>
            <div style="text-align: center; padding: 0 12px;">
                <div style="font-size: 16px; font-weight: 800; color: {ratio_color}; font-family: var(--font-display);">{io_ratio:.2f}</div>
                <div style="font-size: 9px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;">I/O</div>
            </div>
            <div class="risk-badge" style="background: {risk_config['bg']}; color: {risk_config['color']}; border: 1px solid {risk_config['color']}20;">
                {risk_config['label']} RISK
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # KPI CARDS
    # =========================================================================
    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    delta_pct = ((merchant_data['rolling_3d_inflow'] / merchant_data['daily_inflow']) - 1) * 100
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        trend_class = "trend-up" if delta_pct >= 0 else "trend-down"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Daily Inflow</div>
            <div class="kpi-value">₹{merchant_data['daily_inflow']:,.0f}</div>
            <div class="kpi-trend {trend_class}">
                {'↑' if delta_pct >= 0 else '↓'} {abs(delta_pct):.1f}% vs 3d avg
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k2:
        net_positive = merchant_data['net_cash_flow'] >= 0
        net_color = "#059669" if net_positive else "#DC2626"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Net Cash Flow</div>
            <div class="kpi-value" style="color: {net_color};">
                {'+' if net_positive else ''}₹{merchant_data['net_cash_flow']:,.0f}
            </div>
            <div class="kpi-trend {'trend-up' if net_positive else 'trend-down'}">
                {'Positive' if net_positive else 'Negative'} daily balance
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k3:
        buffer_healthy = merchant_data['liquidity_buffer_days'] >= 5
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📅</div>
            <div class="kpi-label">Buffer Days</div>
            <div class="kpi-value">{merchant_data['liquidity_buffer_days']:.1f}</div>
            <div class="kpi-trend {'trend-up' if buffer_healthy else 'trend-down'}">
                {'Healthy' if buffer_healthy else 'Below 5 day target'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k4:
        credit_pct = merchant_data['credit_utilization_ratio'] * 100
        credit_healthy = credit_pct < 70
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💳</div>
            <div class="kpi-label">Credit Utilization</div>
            <div class="kpi-value">{credit_pct:.0f}%</div>
            <div class="kpi-trend {'trend-up' if credit_healthy else 'trend-down'}">
                {'Normal usage' if credit_healthy else 'High utilization'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # RISK ASSESSMENT
    # =========================================================================
    st.markdown('<div class="section-title">Risk Assessment</div>', unsafe_allow_html=True)
    
    risk_col, alert_col = st.columns([1, 1.6])
    
    with risk_col:
        # Compute supplementary stats for the panel
        stress = merchant_data.get('stress_score_composite', 0)
        vol = merchant_data.get('rolling_7d_volatility', 0)
        debt_sr = merchant_data.get('debt_service_ratio', 0)
        
        st.markdown(f"""
        <div class="risk-panel">
            <div class="risk-content">
                <div class="risk-label">Shortage Probability</div>
                <div class="risk-score" style="color: {risk_config['color']};">{int(risk_prob * 100)}</div>
                <div class="risk-level-text">{risk_config['label']} RISK</div>
                <div class="risk-threshold-info">Threshold: {int(threshold * 100)}%</div>
                <div class="risk-bar-bg">
                    <div class="risk-bar-fill" style="width: {max(risk_prob * 100, 2)}%; background: {risk_config['color']};"></div>
                </div>
                <div class="risk-stats-row">
                    <div class="risk-stat-item">
                        <div class="risk-stat-val">{stress:.2f}</div>
                        <div class="risk-stat-lbl">Stress</div>
                    </div>
                    <div class="risk-stat-item">
                        <div class="risk-stat-val">{vol:.2f}</div>
                        <div class="risk-stat-lbl">Volatility</div>
                    </div>
                    <div class="risk-stat-item">
                        <div class="risk-stat-val">{debt_sr:.0%}</div>
                        <div class="risk-stat-lbl">Debt Ratio</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with alert_col:
        # Determine alert config
        if risk_prob >= 0.8:
            alert_bg = "#FEF2F2"
            alert_border = "#DC2626"
            alert_icon = "🚨"
            alert_title_text = "Immediate Action Required"
            alert_desc = risk_config['desc'] + ". Review merchant account and consider intervention strategies."
        elif risk_prob >= 0.6:
            alert_bg = "#FFFBEB"
            alert_border = "#D97706"
            alert_icon = "⚠️"
            alert_title_text = "Attention Needed"
            alert_desc = risk_config['desc'] + ". Monitor trends closely and prepare contingencies."
        elif risk_prob >= 0.4:
            alert_bg = "#F0F9FF"
            alert_border = "#0284C7"
            alert_icon = "ℹ️"
            alert_title_text = "Under Observation"
            alert_desc = risk_config['desc'] + ". Periodic review recommended."
        else:
            alert_bg = "#ECFDF5"
            alert_border = "#059669"
            alert_icon = "✓"
            alert_title_text = "Healthy Status"
            alert_desc = risk_config['desc'] + ". Continue standard monitoring protocols."
        
        # Assessment metrics
        buffer_d = merchant_data.get('liquidity_buffer_days', 0)
        io_r = merchant_data.get('inflow_outflow_ratio', 0)
        cred_u = merchant_data.get('credit_utilization_ratio', 0) * 100
        coverage = merchant_data.get('cashflow_coverage_ratio', 0)
        
        # Card header
        st.markdown(f"""
        <div style="background: #FFFFFF; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04); overflow: hidden;">
            <div style="padding: 14px 22px; border-bottom: 1px solid #E2E8F0; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 13px; font-weight: 700; color: #0F172A;">Risk Summary</span>
                <span style="background: {risk_config['bg']}; color: {risk_config['color']}; border: 1px solid {risk_config['color']}20; font-size: 10px; padding: 4px 10px; border-radius: 100px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">{risk_config['label']}</span>
            </div>
            <div style="padding: 18px 22px;">
                <div style="background: {alert_bg}; border-left: 4px solid {alert_border}; border-radius: 10px; padding: 14px 18px; display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 18px; line-height: 1; flex-shrink: 0; margin-top: 1px;">{alert_icon}</span>
                    <div>
                        <div style="font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 3px;">{alert_title_text}</div>
                        <div style="font-size: 12px; color: #475569; line-height: 1.5;">{alert_desc}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Spacer between Risk Summary card and metric grid
        st.markdown('<div style="margin-top: 14px;"></div>', unsafe_allow_html=True)
        
        # Metric grid using Streamlit columns
        m1, m2, m3, m4 = st.columns(4)
        metric_items = [
            ("Buffer Days", f"{buffer_d:.1f}", '#059669' if buffer_d >= 5 else '#DC2626'),
            ("I/O Ratio", f"{io_r:.2f}", '#059669' if io_r >= 1 else '#DC2626'),
            ("Credit Used", f"{cred_u:.0f}%", '#059669' if cred_u < 70 else '#DC2626'),
            ("Cash Coverage", f"{coverage:.2f}x", '#059669' if coverage >= 1.5 else '#D97706' if coverage >= 1 else '#DC2626'),
        ]
        for mcol, (mlabel, mval, mcolor) in zip([m1, m2, m3, m4], metric_items):
            with mcol:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border-radius: 12px; padding: 16px 14px; border: 1px solid #E2E8F0; text-align: center; box-shadow: 0 1px 2px rgba(0,0,0,0.04); transition: all 0.2s;">
                    <div style="font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">{mlabel}</div>
                    <div style="font-size: 22px; font-weight: 800; color: {mcolor}; font-family: 'DM Sans', sans-serif; line-height: 1;">{mval}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Contributing factors
        if risk_factors:
            chips = "".join([f'<span class="factor-chip">⚠ {f}</span>' for f in risk_factors])
            st.markdown(f"""
            <div style="margin-top: 6px;">
                <div style="font-size: 10px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">Contributing Factors</div>
                <div class="factors-list">{chips}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # =========================================================================
    # CHARTS
    # =========================================================================
    st.markdown('<div class="section-title">Analytics</div>', unsafe_allow_html=True)
    
    chart1, chart2 = st.columns([2, 1])
    
    with chart1:
        st.markdown("""
        <div style="background:#FFFFFF; border-radius:14px; border:1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); padding:24px; margin-bottom:6px;">
            <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px; letter-spacing:-0.01em;">Cash Flow Trend (7 Days)</div>
            <div style="font-size:11px; color:#94A3B8; font-weight:500;">Daily inflow vs outflow with net flow overlay</div>
        </div>
        """, unsafe_allow_html=True)
        cashflow_data = generate_cashflow_data(
            merchant_data['daily_inflow'],
            merchant_data['daily_outflow_estimated'],
            merchant_data['rolling_7d_volatility']
        )
        st.plotly_chart(create_cashflow_chart(cashflow_data), use_container_width=True)
    
    with chart2:
        st.markdown("""
        <div style="background:#FFFFFF; border-radius:14px; border:1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); padding:24px; margin-bottom:6px;">
            <div style="font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px; letter-spacing:-0.01em;">Financial Health Score</div>
            <div style="font-size:11px; color:#94A3B8; font-weight:500;">Multi-dimensional risk radar</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_radar_chart(merchant_data), use_container_width=True)
    
    # =========================================================================
    # DETAILED METRICS TABS
    # =========================================================================
    st.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Liquidity Metrics", "Risk Indicators", "Merchant Profile"])
    
    with tab1:
        l1, l2, l3, l4 = st.columns(4)
        metrics = [
            ("Buffer Ratio", f"{merchant_data['liquidity_buffer_ratio']:.2f}", merchant_data['liquidity_buffer_ratio'] >= 3),
            ("Buffer Days", f"{merchant_data['liquidity_buffer_days']:.1f}", merchant_data['liquidity_buffer_days'] >= 5),
            ("Cash Coverage", f"{merchant_data['cashflow_coverage_ratio']:.2f}x", merchant_data['cashflow_coverage_ratio'] >= 1.5),
            ("Working Capital", f"{merchant_data['working_capital_indicator']:.2f}", merchant_data['working_capital_indicator'] >= 0),
        ]
        for col, (label, value, healthy) in zip([l1, l2, l3, l4], metrics):
            with col:
                status_cls = 'detail-status-healthy' if healthy else 'detail-status-warning'
                st.markdown(f"""
                <div class="detail-card">
                    <div class="detail-status {status_cls}">{'✓' if healthy else '!'}</div>
                    <div class="detail-value">{value}</div>
                    <div class="detail-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        r1, r2, r3, r4 = st.columns(4)
        risk_metrics = [
            ("Credit Util.", f"{merchant_data['credit_utilization_ratio']*100:.0f}%", merchant_data['credit_utilization_ratio'] < 0.7),
            ("Debt Service", f"{merchant_data['debt_service_ratio']*100:.0f}%", merchant_data['debt_service_ratio'] < 0.4),
            ("Stress Score", f"{merchant_data['stress_score_composite']:.2f}", merchant_data['stress_score_composite'] < 0.5),
            ("Volatility", f"{merchant_data['rolling_7d_volatility']:.2f}", merchant_data['rolling_7d_volatility'] < 0.3),
        ]
        for col, (label, value, healthy) in zip([r1, r2, r3, r4], risk_metrics):
            with col:
                status_cls = 'detail-status-healthy' if healthy else 'detail-status-warning'
                st.markdown(f"""
                <div class="detail-card">
                    <div class="detail-status {status_cls}">{'✓' if healthy else '!'}</div>
                    <div class="detail-value">{value}</div>
                    <div class="detail-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        p1, p2, p3, p4 = st.columns(4)
        profile = [
            ("Category", merchant_data['merchant_category'], "🏷️"),
            ("Location", merchant_data['merchant_city'], "📍"),
            ("KYC Status", merchant_data['kyc_status'], "✓"),
            ("Risk Segment", merchant_data['risk_segment_internal'], "📊"),
        ]
        for col, (label, value, icon) in zip([p1, p2, p3, p4], profile):
            with col:
                st.markdown(f"""
                <div class="detail-card">
                    <div class="detail-status detail-status-info">{icon}</div>
                    <div class="detail-value" style="font-size: 15px;">{value}</div>
                    <div class="detail-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # =========================================================================
    # FOOTER
    # =========================================================================
    footer_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    st.markdown(f"""
    <div class="footer">
        <div class="footer-text">
            PocketQuant Risk Intelligence Platform • XGBoost ML Engine • Threshold: {int(threshold * 100)}%
        </div>
        <div class="footer-text">
            © 2026 PocketQuant Analytics • Last Updated: {footer_time}
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
