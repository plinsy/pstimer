"""
Theme management for PSTimer.
"""


class ThemeManager:
    """Manages color themes and styling for the application."""

    THEMES = {
        "csTimer": {
            "name": "csTimer",
            "bg": "#ffffff",
            "secondary_bg": "#f5f5f5",
            "sidebar_bg": "#f0f0f0",
            "panel_bg": "#e8e8e8",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "text_hint": "#999999",
            "accent": "#4CAF50",
            "accent_hover": "#45a049",
            "timer_color": "#333333",
            "timer_ready": "#4CAF50",
            "timer_running": "#FF9800",
            "border": "#ddd",
            "button_bg": "#ffffff",
            "button_hover": "#f5f5f5",
            "font_family": "Segoe UI",
            "mono_font": "Consolas",
        },
        "Dark": {
            "name": "Dark",
            "bg": "#1e1e1e",
            "secondary_bg": "#252526",
            "sidebar_bg": "#2d2d30",
            "panel_bg": "#3c3c3c",
            "text_primary": "#cccccc",
            "text_secondary": "#969696",
            "text_hint": "#6e6e6e",
            "accent": "#007acc",
            "accent_hover": "#005a9e",
            "timer_color": "#ffffff",
            "timer_ready": "#4CAF50",
            "timer_running": "#FF9800",
            "border": "#3c3c3c",
            "button_bg": "#3c3c3c",
            "button_hover": "#4e4e4e",
            "font_family": "Segoe UI",
            "mono_font": "Consolas",
        },
        "Blue": {
            "name": "Blue",
            "bg": "#0d1421",
            "secondary_bg": "#1a2332",
            "sidebar_bg": "#253040",
            "panel_bg": "#2e3d50",
            "text_primary": "#e6f2ff",
            "text_secondary": "#b3d9ff",
            "text_hint": "#7fb3d3",
            "accent": "#4fc3f7",
            "accent_hover": "#29b6f6",
            "timer_color": "#ffffff",
            "timer_ready": "#4CAF50",
            "timer_running": "#FF9800",
            "border": "#2e3d50",
            "button_bg": "#2e3d50",
            "button_hover": "#3a4a5f",
            "font_family": "Segoe UI",
            "mono_font": "Consolas",
        },
    }

    def __init__(self, theme_name="csTimer"):
        self.current_theme_name = theme_name

    def get_theme(self):
        """Get the current theme dictionary."""
        return self.THEMES.get(self.current_theme_name, self.THEMES["csTimer"])

    def set_theme(self, theme_name):
        """Set the current theme."""
        if theme_name in self.THEMES:
            self.current_theme_name = theme_name
            return True
        return False

    def get_available_themes(self):
        """Get list of available theme names."""
        return list(self.THEMES.keys())

    def get_color(self, color_key):
        """Get a specific color from the current theme."""
        theme = self.get_theme()
        return theme.get(color_key, "#000000")

    def get_font(self, font_type="normal"):
        """Get font family for the specified type."""
        theme = self.get_theme()
        if font_type == "mono":
            return theme.get("mono_font", "Consolas")
        return theme.get("font_family", "Segoe UI")
