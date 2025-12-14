"""
Configuration management for Customs Extractor GUI
Handles user preferences, recent files, and settings
"""

import json
import os
from typing import List, Dict, Any
from pathlib import Path


class Config:
    """Manages application configuration and user preferences"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".customs_extractor"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.defaults = {
            "theme": "dark",  # "dark", "light", "system"
            "auto_open": True,
            "show_preview": True,
            "auto_update_output": True,
            "remember_last_folder": True,
            "max_recent_files": 10,
            "default_output_name": "DS hàng",
            "recent_files": [],
            "last_input_folder": "",
            "last_output_folder": "",
            "window_geometry": "900x700"
        }
        
        self.settings = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load settings from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new settings
                    return {**self.defaults, **loaded}
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.defaults.copy()
        return self.defaults.copy()
    
    def save(self):
        """Save current settings to config file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save()
    
    def add_recent_file(self, filepath: str):
        """Add a file to recent files list"""
        recent = self.settings.get("recent_files", [])
        
        # Remove if already exists
        if filepath in recent:
            recent.remove(filepath)
        
        # Add to beginning
        recent.insert(0, filepath)
        
        # Limit to max_recent_files
        max_files = self.settings.get("max_recent_files", 10)
        recent = recent[:max_files]
        
        # Update and save
        self.settings["recent_files"] = recent
        self.save()
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files (only existing ones)"""
        recent = self.settings.get("recent_files", [])
        # Filter out non-existent files
        existing = [f for f in recent if os.path.exists(f)]
        
        # Update if list changed
        if len(existing) != len(recent):
            self.settings["recent_files"] = existing
            self.save()
        
        return existing
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.settings["recent_files"] = []
        self.save()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.defaults.copy()
        self.save()
