import reflex as rx
from typing import Any
from .config import Config
from uudex_api_client.api.participants import get_all_participants
from uudex_api_client.client import Client
import rxconfig


class State(rx.State):
    """The app state."""
    # Store list of participants as dictionaries
    participants: list[dict[str, Any]] = []
    loading: bool = False
    error: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("=== State Initialization ===")
        print(f"REFLEX_BACKEND_PORT: {Config.get_server_url()}")
        print(f"SERVER_MODE: {Config.SERVER_MODE}")

    def navigate(self, route: str):
        """Navigate to a given route."""
        return rx.redirect(route)

    async def get_participants(self):
        """Fetch all participants from the API."""
        self.loading = True
        try:
            # Create client instance with base URL from config
            client = Client(base_url=rxconfig.config.api_url)
            response = await get_all_participants.asyncio(client=client)
            # Convert Participant objects to dictionaries immediately
            self.participants = [{
                "participant_id": p.participant_id,
                "participant_name": p.participant_name,
                "participant_description": p.participant_description,
                "participant_contact": p.participant_contact,
            } for p in response] if response else []
            self.error = ""
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False
