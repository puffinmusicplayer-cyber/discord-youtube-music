"""
Windows Media Session Detector

Detects currently playing media from any app using Windows media controls:
- Apple Music
- YouTube Music (browser or PWA)
- Tidal
- And more
"""

import asyncio
from dataclasses import dataclass
from typing import Optional

try:
    from winrt.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as MediaManager,
        GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
    )
    WINRT_AVAILABLE = True
except ImportError:
    WINRT_AVAILABLE = False
    print("Warning: winrt not installed. Run: pip install winrt-Windows.Media.Control")


@dataclass
class MediaInfo:
    """Current media playback information"""
    title: str
    artist: str
    album: str
    app_id: str
    is_playing: bool
    position_seconds: float = 0.0  # Current playback position
    duration_seconds: float = 0.0  # Total track duration


async def get_media_info() -> Optional[MediaInfo]:
    """
    Get currently playing media information from Windows.

    Returns:
        MediaInfo object if media is playing, None otherwise
    """
    if not WINRT_AVAILABLE:
        return None

    try:
        sessions = await MediaManager.request_async()
        current = sessions.get_current_session()

        if not current:
            return None

        # Get media properties
        info = await current.try_get_media_properties_async()

        # Get playback status
        playback_info = current.get_playback_info()
        is_playing = playback_info.playback_status == PlaybackStatus.PLAYING

        # Get app identifier
        app_id = current.source_app_user_model_id or "unknown"

        # Get timeline info (position and duration)
        position_seconds = 0.0
        duration_seconds = 0.0
        try:
            timeline = current.get_timeline_properties()
            # Convert from TimeSpan (100-nanosecond ticks) to seconds
            # position is current playback position
            # end_time is the total duration of the track
            if hasattr(timeline.position, 'duration'):
                position_seconds = timeline.position.duration / 10_000_000
            if hasattr(timeline.end_time, 'duration'):
                duration_seconds = timeline.end_time.duration / 10_000_000
        except Exception as e:
            pass  # Some apps don't provide timeline info

        return MediaInfo(
            title=info.title or "Unknown Title",
            artist=info.artist or "Unknown Artist",
            album=info.album_title or "",
            app_id=app_id,
            is_playing=is_playing,
            position_seconds=position_seconds,
            duration_seconds=duration_seconds,
        )

    except Exception as e:
        print(f"Error getting media info: {e}")
        return None


async def get_all_sessions():
    """Get all active media sessions (for debugging)"""
    if not WINSDK_AVAILABLE:
        return []

    try:
        sessions = await MediaManager.request_async()
        all_sessions = sessions.get_sessions()

        result = []
        for session in all_sessions:
            info = await session.try_get_media_properties_async()
            result.append({
                "app": session.source_app_user_model_id,
                "title": info.title,
                "artist": info.artist,
            })
        return result
    except Exception as e:
        print(f"Error getting sessions: {e}")
        return []


# Test the detector
if __name__ == "__main__":
    async def test():
        print("Testing media detection...")
        print("Play some music and press Enter")
        input()

        media = await get_media_info()
        if media:
            print(f"\nDetected:")
            print(f"  Title:  {media.title}")
            print(f"  Artist: {media.artist}")
            print(f"  Album:  {media.album}")
            print(f"  App:    {media.app_id}")
            print(f"  Playing: {media.is_playing}")
        else:
            print("No media detected")

        print("\nAll sessions:")
        for s in await get_all_sessions():
            print(f"  - {s['app']}: {s['title']} by {s['artist']}")

    asyncio.run(test())
