# Discord YouTube Music Rich Presence

Show what you're listening to on Discord with **YouTube Music**!

> **Want Apple Music or Tidal support?** Star this repo! At 50 stars I'll add Apple Music, at 100 stars I'll add Tidal.

## Features

- **"Listening to YouTube Music"** status (like Spotify)
- **Album artwork** automatically fetched
- **YouTube Music logo** overlay on album art
- **Pause detection** - shows when you're paused

## Requirements

- Windows 10/11
- Python 3.9+
- Discord desktop app
- YouTube Music (browser or PWA)

## Quick Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and name it **"YouTube Music"**
3. Copy the **Application ID**

### 2. Upload YouTube Music Icon

1. In your Discord app, go to **Rich Presence > Art Assets**
2. Upload the YouTube Music icon with the name: `youtube_music`
   - [Download Icon](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/512px-Youtube_Music_icon.svg.png)
3. Wait 5-10 minutes for Discord to process

### 3. Install & Configure

```bash
# Clone the repo
git clone https://github.com/puffinmusicplayer-cyber/discord-youtube-music.git
cd discord-youtube-music

# Install dependencies
pip install -r requirements.txt

# Create local config with your Application ID
echo 'DISCORD_CLIENT_ID = "YOUR_APPLICATION_ID_HERE"' > config_local.py
```

### 4. Run

```bash
python main.py
```

Play music on YouTube Music and check your Discord profile!

## Configuration

Create `config_local.py` (gitignored):

```python
# Your Discord Application ID
DISCORD_CLIENT_ID = "123456789012345678"

# Optional: Last.fm API key for better album art matching
# Get one free at: https://www.last.fm/api/account/create
LASTFM_API_KEY = None
```

## How It Works

1. **Media Detection**: Uses Windows Media Session API to detect YouTube Music
2. **Album Art**: Fetches artwork from iTunes Search API (free, no key needed)
3. **Discord RPC**: Updates your Discord status via Rich Presence

## Troubleshooting

**"Could not connect to Discord"**
- Make sure Discord desktop app is running
- Restart Discord and try again

**Album art not showing**
- Some songs may not be found in iTunes database
- Add a Last.fm API key in config_local.py for better results

**Icon not showing**
- Make sure you uploaded the icon to Discord Developer Portal
- Icon name must be exactly `youtube_music`
- Wait 5-10 minutes after uploading for Discord to propagate

## Roadmap

- [x] YouTube Music support
- [ ] Apple Music support (at 50 stars)
- [ ] Tidal support (at 100 stars)

## Disclaimer

This project uses Discord's official [Rich Presence API](https://discord.com/developers/docs/rich-presence/overview). It is **not** a selfbot and does not violate Discord's Terms of Service.

YouTube Music is a trademark of Google LLC. This project is not affiliated with or endorsed by Google.

## License

MIT
