import json
import os
import logging
from typing import Dict, Any

class ConfigLoader:
    """Handles loading and managing application configuration"""
    
    def __init__(self):
        """Initialize the configuration loader"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from config.json.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
            
        Raises:
            FileNotFoundError: If config.json doesn't exist
            json.JSONDecodeError: If config.json is invalid
        """
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
            
            if not os.path.exists(config_path):
                self.logger.error(f"Configuration file not found: {config_path}")
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                
            self.logger.info("Configuration loaded successfully")
            return self.config
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key (dot notation supported)
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value or default
        """
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_value(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key (dot notation supported)
            value (Any): Value to set
            
        Returns:
            bool: True if successful
        """
        try:
            keys = key.split('.')
            target = self.config
            
            # Navigate to the nested dictionary
            for k in keys[:-1]:
                if k not in target:
                    target[k] = {}
                target = target[k]
            
            # Set the value
            target[keys[-1]] = value
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting configuration value: {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            bool: True if successful
        """
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
            
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
                
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def validate_config(self) -> bool:
        """
        Validate the configuration structure.
        
        Returns:
            bool: True if configuration is valid
        """
        required_keys = [
            'app_name',
            'version',
            'database',
            'templates',
            'output',
            'gui',
            'logging'
        ]
        
        try:
            for key in required_keys:
                if key not in self.config:
                    self.logger.error(f"Missing required configuration key: {key}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating configuration: {e}")
            return False 