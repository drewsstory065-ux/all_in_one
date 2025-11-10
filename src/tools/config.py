import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # Get the path to config.ini relative to the project root
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')
        config_path = os.path.abspath(config_path)
        self.config.read(config_path)
    
    def get(self, section, key, fallback=None):
        """
        Get a configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value or fallback
        """
        return self.config.get(section, key, fallback=fallback)
    
    def get_int(self, section, key, fallback=0):
        """
        Get an integer configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as int or fallback
        """
        return self.config.getint(section, key, fallback=fallback)
    
    def get_bool(self, section, key, fallback=False):
        """
        Get a boolean configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as bool or fallback
        """
        return self.config.getboolean(section, key, fallback=fallback)
    
    def get_float(self, section, key, fallback=0.0):
        """
        Get a float configuration value.
        
        Args:
            section: The section name in the config file
            key: The key name in the section
            fallback: Default value if key is not found
        
        Returns:
            The configuration value as float or fallback
        """
        return self.config.getfloat(section, key, fallback=fallback)