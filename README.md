# Discord Music Rich Presence

Show what you're listening to on Discord - works with **YouTube Music**, **Apple Music**, **Tidal**, and any media player that integrates with Windows media controls.

## Features

- **"Listening to"** status (like Spotify)
- **Album artwork** automatically fetched from iTunes/MusicBrainz
- **Progress bar** with elapsed/remaining time
- **App icon** (YouTube Music, Apple Music, Tidal logos)
- **Works with any media player** that uses Windows media controls

## Requirements

- Windows 10/11
- Python 3.9+
- Discord desktop app

## Quick Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and name it (e.g., "Music", "Now Playing")
3. Copy the **Application ID**

### 2. Upload App Icons (Optional but Recommended)

1. In your Discord app, go to **Rich Presence > Art Assets**
2. Upload icons with these exact names:
   - `youtube_music` - [Download](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/512px-Youtube_Music_icon.svg.png)
   - `apple_music` - Apple Music logo
   - `tidal` - Tidal logo
3. Wait 5-10 minutes for Discord to process

### 3. Install & Configure

```bash
# Clone the repo
git clone https://github.com/puffinmusicplayer-cyber/discord-youtube-music.git
cd discord-youtube-music

# Install dependencies
pip install -r requirements.txt

# Edit config.py and add your Application ID
# DISCORD_CLIENT_ID = "YOUR_APPLICATION_ID_HERE"
```

### 4. Run

```bash
python main.py
```

Play music and check your Discord profile!

## Configuration

Edit `config.py`:

```python
# Your Discord Application ID
DISCORD_CLIENT_ID = "123456789012345678"

# How often to check for song changes (seconds)
POLL_INTERVAL = 5

# Force a specific app icon (always show YouTube Music, etc.)
# Options: "youtube_music", "apple_music", "tidal", "spotify", or None
FORCE_APP_ICON = "youtube_music"

# Optional: Last.fm API key for better album art matching
# Get one free at: https://www.last.fm/api/account/create
LASTFM_API_KEY = None
```

## How It Works

1. **Media Detection**: Uses Windows Media Session API to detect what's playing
2. **Album Art**: Fetches artwork from iTunes Search API (free, no key needed)
3. **Discord RPC**: Updates your Discord status via Rich Presence

## Supported Music Apps

Any app that integrates with Windows media controls:
- YouTube Music (browser or desktop app)
- Apple Music
- Tidal
- Spotify (though Spotify has its own integration)
- Deezer
- Amazon Music
- Web browsers playing audio
- And more...

## Troubleshooting

**"Could not connect to Discord"**
- Make sure Discord desktop app is running
- Restart Discord and try again

**Album art not showing**
- Some songs may not be found in iTunes database
- Add a Last.fm API key in config.py for better results

**Icon not showing**
- Make sure you uploaded the icon to Discord Developer Portal
- Icon name must match exactly (e.g., `youtube_music`)
- Wait 5-10 minutes after uploading for Discord to propagate

## Disclaimer

This project uses Discord's official [Rich Presence API](https://discord.com/developers/docs/rich-presence/overview), which is designed and documented for exactly this type of use. It is **not** a selfbot, does not violate Discord's Terms of Service, and does not modify the Discord client.

YouTube Music, Apple Music, and Tidal are trademarks of their respective owners (Google LLC, Apple Inc., and TIDAL Music AS). This project is not affiliated with, endorsed by, or sponsored by any of these companies. Logos are used solely to indicate the source of currently playing media.

## License

MIT
