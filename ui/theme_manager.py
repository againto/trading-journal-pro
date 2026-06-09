"""Theme manager for switching between dark and light modes"""

import json
from pathlib import Path
from ui.modern_styles import MODERN_DARK_STYLESHEET, MODERN_LIGHT_STYLESHEET
import logging

logger = logging.getLogger(__name__)

class ThemeManager:
    """Manages application theme switching"""
    
    CONFIG_FILE = "config/theme_config.json"
    
    THEMES = {
        'dark': MODERN_DARK_STYLESHEET,
        'light': MODERN_LIGHT_STYLESHEET
    }
    
    def __init__(self):
        """Initialize theme manager"""
        try:
            self.current_theme = self.load_theme()
            self._ensure_config_dir()
            logger.info(f"Theme manager initialized with theme: {self.current_theme}")
        except Exception as e:
            logger.error(f"Error initializing theme manager: {e}")
            self.current_theme = 'dark'
    
    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        try:
            config_dir = Path("config")
            config_dir.mkdir(exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating config directory: {e}")
    
    def load_theme(self) -> str:
        """
        Load saved theme preference
        
        Returns:
            str: Theme name ('dark' or 'light')
        """
        try:
            if Path(self.CONFIG_FILE).exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    theme = config.get('theme', 'dark')
                    if theme not in self.THEMES:
                        logger.warning(f"Unknown theme '{theme}', using 'dark'")
                        return 'dark'
                    return theme
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding theme config: {e}")
        except Exception as e:
            logger.error(f"Error loading theme: {e}")
        
        return 'dark'  # Default to dark theme
    
    def save_theme(self, theme: str):
        """
        Save theme preference
        
        Args:
            theme: Theme name to save ('dark' or 'light')
        """
        if theme not in self.THEMES:
            logger.error(f"Invalid theme: {theme}")
            return
        
        try:
            self._ensure_config_dir()
            config = {'theme': theme}
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            self.current_theme = theme
            logger.info(f"Theme saved: {theme}")
        except Exception as e:
            logger.error(f"Error saving theme: {e}")
    
    def get_stylesheet(self, theme: str = None) -> str:
        """
        Get stylesheet for a theme
        
        Args:
            theme: Theme name (optional, uses current if not provided)
            
        Returns:
            str: Stylesheet string
        """
        theme = theme or self.current_theme
        if theme not in self.THEMES:
            logger.warning(f"Unknown theme '{theme}', using 'dark'")
            return self.THEMES.get('dark', '')
        return self.THEMES.get(theme, '')
    
    def toggle_theme(self) -> str:
        """
        Toggle between dark and light theme
        
        Returns:
            str: New theme name
        """
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.save_theme(new_theme)
        logger.info(f"Theme toggled to: {new_theme}")
        return new_theme
    
    def is_dark_theme(self) -> bool:
        """Check if current theme is dark"""
        return self.current_theme == 'dark'
    
    def is_light_theme(self) -> bool:
        """Check if current theme is light"""
        return self.current_theme == 'light'
