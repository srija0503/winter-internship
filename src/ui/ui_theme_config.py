# UI/UX THEME CONFIGURATION

PRIMARY_COLOR = "#ff4b4b"       # Red Warning
ACCENT_COLOR = "#4ecdc4"        # Medical Teal
BACKGROUND_COLOR = "#ffffff"    # Pure White
TEXT_COLOR = "#2c3e50"          # Dark Slate Blue

# Glassmorphism style (for CSS-in-JS, or export as string)
GLASS_STYLE = """
background: rgba(255, 255, 255, 0.65);
backdrop-filter: blur(12px);
border-radius: 20px;
border: 1px solid rgba(255, 255, 255, 0.18);
box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
"""

FONT_FAMILY = "Outfit, sans-serif"

def export_as_dict():
    """Export theme tokens as dict for use elsewhere (optional utility)"""
    return {
        "colors": {
            "primary": PRIMARY_COLOR,
            "accent": ACCENT_COLOR,
            "background": BACKGROUND_COLOR,
            "text": TEXT_COLOR
        },
        "font": FONT_FAMILY,
        "glass_style": GLASS_STYLE
    }