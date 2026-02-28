"""
Discord Music Rich Presence

Detects music playing on Windows and shows it on your Discord profile.
Supports: Apple Music, YouTube Music, Tidal, and more.

Usage:
    python main.py
"""

import asyncio
import time
import sys

from config import POLL_INTERVAL
from media_detector import get_media_info
from album_art import get_art
from discord_rpc import DiscordRPC


class MusicPresence:
    """Main application class"""

    def __init__(self):
        self.rpc = DiscordRPC()
        self.last_song = None
        self.song_start_time = None
        self.running = False

    def run(self):
        """Main loop - detect media and update Discord"""
        print("=" * 50)
        print("  Discord Music Rich Presence")
        print("=" * 50)
        print()

        # Connect to Discord
        if not self.rpc.connect():
            print("\nCould not connect to Discord.")
            print("Make sure Discord is running and try again.")
            return

        print(f"Polling every {POLL_INTERVAL} seconds...")
        print("Play some music to see it on your Discord profile!")
        print("Press Ctrl+C to stop.\n")

        self.running = True

        try:
            while self.running:
                self._check_media()
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.rpc.clear()
            self.rpc.disconnect()
            print("Disconnected from Discord.")

    def _check_media(self):
        """Check current media and update Discord if changed"""
        # Run async media detection in a new event loop
        media = asyncio.run(get_media_info())

        if media and media.is_playing:
            # Create unique song identifier
            song_id = f"{media.title}|{media.artist}"

            # Update on new song OR periodically for progress bar accuracy
            is_new_song = song_id != self.last_song

            if is_new_song:
                self.last_song = song_id
                duration_str = ""
                if media.duration_seconds > 0:
                    mins = int(media.duration_seconds // 60)
                    secs = int(media.duration_seconds % 60)
                    duration_str = f" ({mins}:{secs:02d})"
                print(f"Now playing: {media.title} - {media.artist}{duration_str}")

            # Try to get album art (only on new song to avoid API spam)
            if is_new_song:
                self._current_art = get_art(media.artist, media.album, media.title)

            # Update Discord with current position for progress bar
            self.rpc.update(
                title=media.title,
                artist=media.artist,
                album=media.album,
                art_url=getattr(self, '_current_art', None),
                position_seconds=media.position_seconds,
                duration_seconds=media.duration_seconds,
                app_id=media.app_id,
            )

        elif self.last_song:
            # Music stopped
            print("Playback stopped")
            self.rpc.clear()
            self.last_song = None
            self._current_art = None


def main():
    """Entry point"""
    app = MusicPresence()
    app.run()


if __name__ == "__main__":
    main()
