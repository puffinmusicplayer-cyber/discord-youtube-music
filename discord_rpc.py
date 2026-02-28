"""
Discord Rich Presence Wrapper

Handles connection to Discord and updating presence status.
"""

import time
from typing import Optional
from pypresence import Presence, exceptions as rpc_exceptions
from pypresence.types import ActivityType

from config import DISCORD_CLIENT_ID, FORCE_APP_ICON


class DiscordRPC:
    """Wrapper for Discord Rich Presence connection"""

    def __init__(self, client_id: str = DISCORD_CLIENT_ID):
        self.client_id = client_id
        self.rpc: Optional[Presence] = None
        self.connected = False
        self.last_update = None

    def connect(self) -> bool:
        """
        Connect to Discord.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            print("Connected to Discord!")
            return True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            print("Make sure Discord is running.")
            self.connected = False
            return False

    def update(
        self,
        title: str,
        artist: str,
        album: Optional[str] = None,
        art_url: Optional[str] = None,
        position_seconds: float = 0.0,
        duration_seconds: float = 0.0,
        app_id: str = "",
    ) -> bool:
        """
        Update Discord presence with current song.

        Args:
            title: Song title
            artist: Artist name
            album: Album name (optional)
            art_url: URL to album art (optional)
            position_seconds: Current playback position in seconds
            duration_seconds: Total track duration in seconds

        Returns:
            True if updated successfully, False otherwise
        """
        if not self.connected or not self.rpc:
            return False

        try:
            # Build presence data with "Listening to" activity type
            presence_data = {
                "activity_type": ActivityType.LISTENING,
                "details": title[:128],  # Discord limit
                "state": f"by {artist}"[:128],
            }

            # Add progress bar timestamps if duration is available
            if duration_seconds > 0:
                now = time.time()
                start_timestamp = int(now - position_seconds)
                end_timestamp = int(now + (duration_seconds - position_seconds))
                presence_data["start"] = start_timestamp
                presence_data["end"] = end_timestamp

            # Add album art if available
            if art_url:
                presence_data["large_image"] = art_url
                if album:
                    presence_data["large_text"] = album[:128]
            else:
                # Use a default music icon (you can upload one in Discord Developer Portal)
                presence_data["large_image"] = "music_icon"
                presence_data["large_text"] = album[:128] if album else "Listening to Music"

            # Add small icon based on music app (like Spotify logo)
            # These need to be uploaded to Discord Developer Portal > Rich Presence > Art Assets
            small_icon = self._get_app_icon(app_id)
            if small_icon:
                presence_data["small_image"] = small_icon
                presence_data["small_text"] = self._get_app_name(app_id)

            self.rpc.update(**presence_data)
            self.last_update = time.time()
            return True

        except rpc_exceptions.InvalidID:
            print("Invalid Discord Application ID")
            self.connected = False
            return False
        except Exception as e:
            print(f"Error updating presence: {e}")
            return False

    def clear(self) -> bool:
        """
        Clear Discord presence (when music stops).

        Returns:
            True if cleared successfully, False otherwise
        """
        if not self.connected or not self.rpc:
            return False

        try:
            self.rpc.clear()
            self.last_update = None
            return True
        except Exception as e:
            print(f"Error clearing presence: {e}")
            return False

    def disconnect(self):
        """Disconnect from Discord"""
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
        self.connected = False
        self.rpc = None

    def _get_app_icon(self, app_id: str) -> Optional[str]:
        """
        Get the small icon name for a music app.
        Icons must be uploaded to Discord Developer Portal > Rich Presence > Art Assets.
        """
        # Use forced icon if configured (always show YouTube Music, etc.)
        if FORCE_APP_ICON:
            return FORCE_APP_ICON

        app_id_lower = app_id.lower()

        # Map app IDs to icon names (upload these to your Discord app)
        if "youtube" in app_id_lower or "music.ui" in app_id_lower:
            return "youtube_music"
        elif "apple" in app_id_lower or "itunes" in app_id_lower:
            return "apple_music"
        elif "tidal" in app_id_lower:
            return "tidal"
        elif "spotify" in app_id_lower:
            return "spotify"
        elif "chrome" in app_id_lower or "msedge" in app_id_lower:
            # Browser - likely YouTube Music
            return "youtube_music"

        return None

    def _get_app_name(self, app_id: str) -> str:
        """Get the display name for a music app."""
        # Use forced icon name if configured
        if FORCE_APP_ICON:
            icon_names = {
                "youtube_music": "YouTube Music",
                "apple_music": "Apple Music",
                "tidal": "TIDAL",
                "spotify": "Spotify",
            }
            return icon_names.get(FORCE_APP_ICON, "Music Player")

        app_id_lower = app_id.lower()

        if "youtube" in app_id_lower or "music.ui" in app_id_lower:
            return "YouTube Music"
        elif "apple" in app_id_lower or "itunes" in app_id_lower:
            return "Apple Music"
        elif "tidal" in app_id_lower:
            return "TIDAL"
        elif "spotify" in app_id_lower:
            return "Spotify"
        elif "chrome" in app_id_lower:
            return "Chrome"
        elif "msedge" in app_id_lower:
            return "Edge"

        return "Music Player"


# Test
if __name__ == "__main__":
    print("Testing Discord RPC connection...")
    print(f"Using Client ID: {DISCORD_CLIENT_ID}")

    rpc = DiscordRPC()
    if rpc.connect():
        print("Updating presence with test data...")
        rpc.update(
            title="Test Song",
            artist="Test Artist",
            album="Test Album",
            start_time=time.time(),
        )
        print("Check your Discord profile! Press Enter to clear and exit.")
        input()
        rpc.clear()
        rpc.disconnect()
    else:
        print("Could not connect to Discord. Is it running?")
