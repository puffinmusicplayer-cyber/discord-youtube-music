"""
Discord Music RPC Configuration

For local development, create config.local.py with your actual credentials.
That file is gitignored and won't be committed.
"""

# Default values (override in config.local.py)
DISCORD_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
POLL_INTERVAL = 3  # Check every 3 seconds (balance between responsive and stable)
LASTFM_API_KEY = None
FORCE_APP_ICON = "youtube_music"
MUSIC_APPS = [
    "AppleInc.AppleMusic",
    "Apple.Music",
    "TIDAL.TIDAL",
    "chrome",
    "msedge",
    "Music.UI",
]

# Try to load local config (overrides defaults above)
try:
    from config_local import *
except ImportError:
    pass
