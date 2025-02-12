"""UUDEX Web Client Application"""

import reflex as rx
from uudex_api_client.api.participants import get_all_participants
from uudex_api_client.models import Participant
from uudex_api_client.client import Client
import rxconfig
from typing import List, Dict, Any


class State(rx.State):
    """The app state."""

    # Store list of participants as dictionaries
    participants: List[Dict[str, Any]] = []
    loading: bool = False
    error: str = ""

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


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("UUDEX Web Client", size="9"),
            rx.button(
                "Load Participants",
                on_click=State.get_participants,
                is_loading=State.loading,
            ),
            rx.cond(
                State.error != "",
                rx.text(State.error, color="red"),
            ),
            rx.data_table(
                data=State.participants,
                columns=[
                    {
                        "field": "participant_id",
                        "name": "ID"
                    },
                    {
                        "field": "participant_name",
                        "name": "Name"
                    },
                    {
                        "field": "participant_description",
                        "name": "Description"
                    },
                    {
                        "field": "participant_contact",
                        "name": "Contact"
                    },
                ],
                pagination=True,
                search=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App(style={"font_family": "Inter"})
app.add_page(index)
