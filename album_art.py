"""
Album Art Fetcher

Fetches album artwork from multiple sources:
1. MusicBrainz + Cover Art Archive (free, no API key)
2. Last.fm API (optional, needs API key for better results)
3. iTunes Search API (free, no API key)
"""

import requests
from typing import Optional
from functools import lru_cache
import hashlib
import time

from config import LASTFM_API_KEY

# Rate limiting for MusicBrainz (requires 1 req/sec)
_last_mb_request = 0


@lru_cache(maxsize=100)
def get_itunes_art(artist: str, track: str) -> Optional[str]:
    """
    Fetch album art from iTunes Search API (free, no key needed).
    Returns high-res artwork URL.
    """
    if not artist or not track:
        return None

    try:
        url = "https://itunes.apple.com/search"
        params = {
            "term": f"{artist} {track}",
            "media": "music",
            "limit": 1,
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        results = data.get("results", [])
        if results:
            # Get artwork and upscale to 600x600
            art_url = results[0].get("artworkUrl100", "")
            if art_url:
                # Replace 100x100 with 600x600 for higher res
                return art_url.replace("100x100", "600x600")

        return None

    except Exception as e:
        print(f"Error fetching iTunes art: {e}")
        return None


@lru_cache(maxsize=100)
def get_musicbrainz_art(artist: str, album: str) -> Optional[str]:
    """
    Fetch album art from MusicBrainz + Cover Art Archive (free, no key).
    """
    global _last_mb_request

    if not artist or not album:
        return None

    try:
        # Rate limit: 1 request per second
        now = time.time()
        if now - _last_mb_request < 1.1:
            time.sleep(1.1 - (now - _last_mb_request))
        _last_mb_request = time.time()

        # Search for release
        url = "https://musicbrainz.org/ws/2/release/"
        params = {
            "query": f'artist:"{artist}" AND release:"{album}"',
            "fmt": "json",
            "limit": 1,
        }
        headers = {
            "User-Agent": "DiscordMusicRPC/1.0 (https://github.com/discord-music-rpc)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()

        releases = data.get("releases", [])
        if not releases:
            return None

        release_id = releases[0].get("id")
        if not release_id:
            return None

        # Get cover art from Cover Art Archive
        _last_mb_request = time.time()
        art_url = f"https://coverartarchive.org/release/{release_id}/front-500"

        # Check if image exists
        response = requests.head(art_url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            return art_url

        return None

    except Exception as e:
        return None


@lru_cache(maxsize=100)
def get_lastfm_art(artist: str, album: str) -> Optional[str]:
    """
    Fetch album art URL from Last.fm (requires API key).
    """
    if not LASTFM_API_KEY:
        return None

    if not artist or not album:
        return None

    try:
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "album.getinfo",
            "api_key": LASTFM_API_KEY,
            "artist": artist,
            "album": album,
            "format": "json",
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        images = data.get("album", {}).get("image", [])

        # Get largest image (extralarge)
        for img in reversed(images):
            if img.get("#text"):
                return img["#text"]

        return None

    except Exception as e:
        return None


@lru_cache(maxsize=100)
def get_lastfm_track_art(artist: str, track: str) -> Optional[str]:
    """
    Fetch track art URL from Last.fm.
    """
    if not LASTFM_API_KEY:
        return None

    if not artist or not track:
        return None

    try:
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.getinfo",
            "api_key": LASTFM_API_KEY,
            "artist": artist,
            "track": track,
            "format": "json",
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        album_images = data.get("track", {}).get("album", {}).get("image", [])
        for img in reversed(album_images):
            if img.get("#text"):
                return img["#text"]

        return None

    except Exception as e:
        return None


def get_art(artist: str, album: str, track: str) -> Optional[str]:
    """
    Get artwork from multiple sources (prioritized).

    Order:
    1. iTunes (fast, high-res, no key needed)
    2. Last.fm album (if API key configured)
    3. Last.fm track (if API key configured)
    4. MusicBrainz (slower due to rate limiting)
    """
    # 1. Try iTunes first (fastest, no key needed)
    art = get_itunes_art(artist, track)
    if art:
        return art

    # 2. Try Last.fm album
    art = get_lastfm_art(artist, album)
    if art:
        return art

    # 3. Try Last.fm track
    art = get_lastfm_track_art(artist, track)
    if art:
        return art

    # 4. Try MusicBrainz (slowest due to rate limit)
    art = get_musicbrainz_art(artist, album)
    if art:
        return art

    return None


# Test
if __name__ == "__main__":
    print("Testing album art fetcher...")
    print()

    # Test with a known song
    test_artist = "Daft Punk"
    test_album = "Random Access Memories"
    test_track = "Get Lucky"

    print(f"Searching for: {test_artist} - {test_track}")
    print()

    print("1. iTunes Search...")
    art = get_itunes_art(test_artist, test_track)
    print(f"   Result: {art}")
    print()

    if LASTFM_API_KEY:
        print("2. Last.fm Album...")
        art = get_lastfm_art(test_artist, test_album)
        print(f"   Result: {art}")
    else:
        print("2. Last.fm: Skipped (no API key)")
    print()

    print("3. MusicBrainz...")
    art = get_musicbrainz_art(test_artist, test_album)
    print(f"   Result: {art}")
    print()

    print("Combined get_art():")
    art = get_art(test_artist, test_album, test_track)
    print(f"   Result: {art}")
