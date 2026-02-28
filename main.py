"""
Discord Music Rich Presence

Detects music playing on Windows and shows it on your Discord profile.
Supports: Apple Music, YouTube Music, Tidal, and more.

Usage:
    python main.py
"""

import asyncio
import time

from config import POLL_INTERVAL
from media_detector import get_media_info
from album_art import get_art
from discord_rpc import DiscordRPC


class MusicPresence:
    """Main application class"""

    def __init__(self):
        self.rpc = DiscordRPC()
        self.current_song_id = None
        self._current_art = None
        self.running = False
        self.pause_count = 0
        self.is_paused = False

        # Store timestamps - NEVER recalculate for same song
        self.song_start_ts = None
        self.song_end_ts = None

    def run(self):
        """Main loop - detect media and update Discord"""
        print("=" * 50)
        print("  Discord Music Rich Presence")
        print("=" * 50)
        print()

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
        """Check current media and update Discord"""
        media = asyncio.run(get_media_info())

        if media and media.is_playing:
            self.pause_count = 0
            song_id = f"{media.title}|{media.artist}"

            # Check if this is a NEW song
            is_new_song = song_id != self.current_song_id

            # Check if resuming from pause (same song)
            is_resume = self.is_paused and song_id == self.current_song_id

            if is_new_song:
                # NEW SONG - calculate fresh timestamps and fetch art
                self.current_song_id = song_id
                self.is_paused = False

                # Calculate timestamps ONCE and store them
                now = int(time.time())
                position = int(media.position_seconds)
                duration = int(media.duration_seconds)
                self.song_start_ts = now - position
                self.song_end_ts = self.song_start_ts + duration if duration > 0 else None

                # Fetch album art FIRST (before Discord update)
                self._current_art = get_art(media.artist, media.album, media.title)

                # Log
                duration_str = ""
                if duration > 0:
                    mins = duration // 60
                    secs = duration % 60
                    duration_str = f" ({mins}:{secs:02d})"
                print(f"Now playing: {media.title} - {media.artist}{duration_str}")

                # Send ONE update to Discord with all data
                self.rpc.update(
                    title=media.title,
                    artist=media.artist,
                    album=media.album,
                    art_url=self._current_art,
                    start_timestamp=self.song_start_ts,
                    end_timestamp=self.song_end_ts,
                    app_id=media.app_id,
                )
                print(f"  -> Discord updated (pos:{position}s, dur:{duration}s)")

            elif is_resume:
                # RESUME - recalculate timestamps for new position
                self.is_paused = False
                print(f"Resumed: {media.title}")

                # Recalculate timestamps based on current position
                now = int(time.time())
                position = int(media.position_seconds)
                duration = int(media.duration_seconds)
                self.song_start_ts = now - position
                self.song_end_ts = self.song_start_ts + duration if duration > 0 else None

                # Send update with stored art and new timestamps
                self.rpc.update(
                    title=media.title,
                    artist=media.artist,
                    album=media.album,
                    art_url=self._current_art,
                    start_timestamp=self.song_start_ts,
                    end_timestamp=self.song_end_ts,
                    app_id=media.app_id,
                )
                print(f"  -> Discord updated (resumed at {position}s)")

            # else: same song, still playing - do nothing (let Discord handle timer)

        elif media and not media.is_playing:
            # Paused - update Discord to stop the timer
            if not self.is_paused:
                self.is_paused = True
                print(f"Paused: {media.title}")

                # Send update with paused=True (removes timer)
                self.rpc.update(
                    title=media.title,
                    artist=media.artist,
                    album=media.album,
                    art_url=self._current_art,
                    start_timestamp=None,  # No timestamp when paused
                    end_timestamp=None,
                    app_id=media.app_id,
                    paused=True,
                )
                print("  -> Timer paused")

            self.pause_count += 1
            # Clear after ~60 seconds of pause
            if self.pause_count > 20 and self.current_song_id:
                print("Paused for too long, clearing presence")
                self.rpc.clear()
                self.current_song_id = None
                self.song_start_ts = None
                self.song_end_ts = None

        else:
            # No media at all
            if self.current_song_id:
                self.pause_count += 1
                if self.pause_count > 3:
                    print("No media, clearing presence")
                    self.rpc.clear()
                    self.current_song_id = None
                    self._current_art = None
                    self.is_paused = False
                    self.song_start_ts = None
                    self.song_end_ts = None


def main():
    app = MusicPresence()
    app.run()


if __name__ == "__main__":
    main()
