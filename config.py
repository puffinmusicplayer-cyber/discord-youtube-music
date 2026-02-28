"""
Discord Music RPC Configuration
"""

# Discord Application ID (from https://discord.com/developers/applications)
DISCORD_CLIENT_ID = "YOUR_CLIENT_ID_HERE"

# How often to check for media changes (seconds)
POLL_INTERVAL = 5

# Last.fm API key (optional - for album art)
# Get one free at: https://www.last.fm/api/account/create
LASTFM_API_KEY = None  # Set to your API key string, e.g., "abc123..."

# Force a specific app icon to always show (overrides auto-detection)
# Options: "youtube_music", "apple_music", "tidal", "spotify", or None for auto-detect
FORCE_APP_ICON = "youtube_music"

# Music apps to detect (app ID patterns)
# These are matched against source_app_user_model_id
MUSIC_APPS = [
    "AppleInc.AppleMusic",
    "Apple.Music",
    "TIDAL.TIDAL",
    "chrome",  # YouTube Music in Chrome
    "msedge",  # YouTube Music in Edge
    "Music.UI",  # YouTube Music PWA
]
