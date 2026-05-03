import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration for Quirky_Dweed."""
    
    # App Settings
    APP_TITLE = "Quirky_Dweed"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Your ultimate hub for anime, manga, manhwa characters, power scaling, and quirky otaku culture."
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    # Feature Flags
    ENABLE_REALTIME = True
    
    @classmethod
    def validate(cls):
        """Validate critical configuration."""
        if not cls.SUPABASE_URL or not cls.SUPABASE_ANON_KEY:
            print("WARNING: Supabase credentials not found. Database features will be disabled.")
            return False
        return True

config = Config()
