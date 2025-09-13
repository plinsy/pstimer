"""
Test theme system and color management.
"""

import pytest
from src.themes import ThemeManager


class TestThemeManager:
    """Test theme management functionality."""

    def test_theme_manager_creation(self, theme_manager):
        """Test ThemeManager initialization."""
        assert theme_manager.current_theme == "csTimer"
        assert theme_manager.get_theme() is not None

    def test_available_themes(self, theme_manager):
        """Test that all expected themes are available."""
        themes = theme_manager.get_available_themes()
        expected_themes = ["csTimer", "Dark", "Blue"]
        
        for theme in expected_themes:
            assert theme in themes, f"Theme '{theme}' not found in available themes"

    def test_theme_switching(self, theme_manager):
        """Test switching between themes."""
        # Switch to Dark theme
        theme_manager.set_theme("Dark")
        assert theme_manager.current_theme == "Dark"
        
        # Switch to Blue theme
        theme_manager.set_theme("Blue")
        assert theme_manager.current_theme == "Blue"
        
        # Switch back to csTimer
        theme_manager.set_theme("csTimer")
        assert theme_manager.current_theme == "csTimer"

    def test_invalid_theme(self, theme_manager):
        """Test setting an invalid theme."""
        original_theme = theme_manager.current_theme
        
        # Try to set invalid theme
        theme_manager.set_theme("NonExistentTheme")
        
        # Should remain on original theme
        assert theme_manager.current_theme == original_theme

    def test_theme_properties(self, theme_manager):
        """Test that all themes have required properties."""
        required_keys = [
            "bg", "text_primary", "timer_color", "timer_ready", "timer_running",
            "border", "font_family", "mono_font"
        ]
        
        for theme_name in theme_manager.get_available_themes():
            theme_manager.set_theme(theme_name)
            theme = theme_manager.get_theme()
            
            for key in required_keys:
                assert key in theme, f"Theme '{theme_name}' missing key '{key}'"
                assert theme[key] is not None, f"Theme '{theme_name}' has None value for '{key}'"

    def test_color_format(self, theme_manager):
        """Test that colors are in valid format."""
        import re
        color_pattern = re.compile(r'^#[0-9a-fA-F]{6}$')
        
        for theme_name in theme_manager.get_available_themes():
            theme_manager.set_theme(theme_name)
            theme = theme_manager.get_theme()
            
            color_keys = [k for k in theme.keys() if 
                         any(color_word in k.lower() for color_word in 
                             ['color', 'bg', 'border', 'accent', 'text'])]
            
            for key in color_keys:
                if key not in ['font_family', 'mono_font']:  # Skip font keys
                    color_value = theme[key]
                    assert color_pattern.match(color_value), \
                        f"Invalid color format in {theme_name}.{key}: {color_value}"

    @pytest.mark.parametrize("theme_name", ["csTimer", "Dark", "Blue"])
    def test_individual_themes(self, theme_manager, theme_name):
        """Test each theme individually."""
        theme_manager.set_theme(theme_name)
        theme = theme_manager.get_theme()
        
        # Check basic structure
        assert isinstance(theme, dict)
        assert len(theme) > 10  # Should have reasonable number of properties
        
        # Check name matches
        assert theme.get("name") == theme_name

    def test_theme_consistency(self, theme_manager):
        """Test that theme switching is consistent."""
        # Get initial theme
        initial_theme = theme_manager.get_theme().copy()
        
        # Switch to different theme and back
        theme_manager.set_theme("Dark")
        theme_manager.set_theme("csTimer")
        
        # Should be identical to initial theme
        current_theme = theme_manager.get_theme()
        assert current_theme == initial_theme

    def test_theme_immutability(self, theme_manager):
        """Test that returned theme dict doesn't affect internal state."""
        theme = theme_manager.get_theme()
        original_bg = theme["bg"]
        
        # Modify returned dict
        theme["bg"] = "#000000"
        
        # Get theme again - should be unchanged
        new_theme = theme_manager.get_theme()
        assert new_theme["bg"] == original_bg

    def test_dark_theme_properties(self, theme_manager):
        """Test specific properties of dark theme."""
        theme_manager.set_theme("Dark")
        theme = theme_manager.get_theme()
        
        # Dark theme should have dark background
        bg_color = theme["bg"]
        assert bg_color.lower() in ["#1e1e1e", "#2d2d30"] or \
               bg_color.startswith("#1") or bg_color.startswith("#2"), \
               f"Dark theme background not dark enough: {bg_color}"

    def test_cstimer_theme_properties(self, theme_manager):
        """Test specific properties of csTimer theme."""
        theme_manager.set_theme("csTimer")
        theme = theme_manager.get_theme()
        
        # csTimer theme should have light background
        bg_color = theme["bg"]
        assert bg_color.lower() in ["#ffffff", "#f5f5f5"] or \
               bg_color.startswith("#f"), \
               f"csTimer theme background not light enough: {bg_color}"
