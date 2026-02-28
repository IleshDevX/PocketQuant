"""
PocketQuant Dashboard Configuration
Enterprise-Grade FinTech Dashboard Theme
Version 3.0
"""

# ==================== COLOR PALETTE ====================
# Sophisticated FinTech Design System
# Trust • Intelligence • Clarity

COLORS = {
    # Primary Brand - Deep Teal (Trust & Stability)
    "primary": "#0D9488",          # Teal - primary accent
    "primary_dark": "#0F766E",     # Deep teal
    "primary_light": "#5EEAD4",    # Light teal
    "primary_subtle": "#CCFBF1",   # Very light teal
    
    # Secondary - Indigo (Intelligence)
    "secondary": "#6366F1",        # Indigo accent
    "secondary_dark": "#4F46E5",   # Deep indigo
    
    # Background Colors
    "bg_main": "#FAFBFC",          # Off-white main background
    "bg_secondary": "#F1F5F9",     # Light slate secondary
    "bg_card": "#FFFFFF",          # Pure white cards
    "bg_dark": "#0F172A",          # Deep navy for headers
    "bg_elevated": "#F8FAFC",      # Elevated surfaces
    
    # Text Colors
    "text_primary": "#0F172A",     # Near black - primary text
    "text_secondary": "#475569",   # Slate - secondary text
    "text_tertiary": "#94A3B8",    # Light slate - tertiary
    "text_muted": "#94A3B8",       # Muted text
    "text_inverse": "#F8FAFC",     # White text on dark
    
    # Semantic Status Colors
    "success": "#059669",          # Emerald green
    "success_bg": "#ECFDF5",       # Light emerald background
    "warning": "#D97706",          # Amber
    "warning_bg": "#FFFBEB",       # Light amber background
    "danger": "#DC2626",           # Red
    "danger_bg": "#FEF2F2",        # Light red background
    "info": "#0284C7",             # Sky blue
    "info_bg": "#F0F9FF",          # Light sky background
    
    # Border Colors
    "border": "#E2E8F0",           # Light border
    "border_dark": "#CBD5E1",      # Darker border
    "divider": "#E2E8F0",          # Divider lines
}

# Risk Level Configuration
RISK_COLORS = {
    "critical": "#DC2626",         # Red - Critical risk
    "high": "#EA580C",             # Orange-red - High risk
    "moderate": "#D97706",         # Amber - Moderate risk
    "low": "#10B981",              # Emerald - Low risk
    "minimal": "#059669",          # Green - Minimal risk
}

# Chart color sequence
CHART_COLORS = [
    "#3B82F6",  # Blue
    "#10B981",  # Green
    "#F59E0B",  # Amber
    "#EF4444",  # Red
    "#8B5CF6",  # Purple
    "#EC4899",  # Pink
    "#06B6D4",  # Cyan
]

# ==================== API CONFIGURATION ====================
API_BASE_URL = "http://localhost:8000"

# ==================== DASHBOARD SETTINGS ====================
PAGE_TITLE = "PocketQuant | Risk Intelligence"
PAGE_ICON = "📊"
LAYOUT = "wide"
