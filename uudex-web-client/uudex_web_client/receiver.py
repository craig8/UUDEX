import reflex as rx
import os
import time
from typing import Dict, List
from datetime import datetime
from .certificate_state import CertificateState


class ReceiverState(rx.State):
    """State for the file receiver page."""

    # State variables
    entity_name: str = ""
    is_polling: bool = False
    polling_interval: int = 10  # seconds
    status_message: str = ""
    show_status: bool = False
    status_is_error: bool = False
    download_dir: str = "downloads"

    # File list - specify the type with .to()
    received_files: List[Dict[str, str]] = [
        {
            "filename": "sample.pdf",
            "sender": "Entity A",
            "received": "2023-09-15 10:30",
            "size": "2.4 MB"
        },
        {
            "filename": "test.csv",
            "sender": "Entity B",
            "received": "2023-09-15 09:45",
            "size": "1.1 MB"
        },
    ]

    def set_entity(self, entity: str):
        """Set the entity to use for receiving files."""
        self.entity_name = entity
        self.status_message = f"Selected {entity} as the receiving entity"
        self.show_status = True
        self.status_is_error = False

    async def start_polling(self):
        """Start polling for new files."""
        if not self.entity_name:
            self.status_message = "Please select an entity first"
            self.show_status = True
            self.status_is_error = True
            return

        self.is_polling = True
        self.status_message = f"Started polling for new files as {self.entity_name}"
        self.show_status = True
        self.status_is_error = False

        # Ensure download directory exists
        os.makedirs(self.download_dir, exist_ok=True)

        # In a real implementation, we would set up a background task
        # For now, we'll simulate with a loop that checks periodically
        await self.poll_once()

    def stop_polling(self):
        """Stop polling for new files."""
        self.is_polling = False
        self.status_message = "Stopped polling for new files"
        self.show_status = True
        self.status_is_error = False

    async def poll_once(self):
        """Poll for new files once."""
        try:
            # Get certificate path for this entity
            cert_path = CertificateState.entity_cert_mapping.get(
                self.entity_name)

            # In a real implementation, we'd create an authenticated client and call the API
            # client = AuthenticatedClient(
            #     base_url="https://your-uudex-server.com",
            #     token=self.get_token_from_cert(cert_path),
            # )

            # Get subscriptions for this entity
            # subscriptions = await client.get_subscriptions()

            # Check each subscription for new data
            # for subscription in subscriptions:
            #     messages = await client.get_messages(subscription.id)
            #     for message in messages:
            #         if not self.is_polling:
            #             return
            #         await self.process_message(message)

            # For demonstration, simulate receiving a file
            await rx.sleep(2)  # Simulate network delay

            if self.is_polling:  # Only add if we're still polling
                # Add a simulated new file
                new_file = {
                    "filename": f"data_{int(time.time())}.xlsx",
                    "sender": "Entity C",
                    "received": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "size": "3.2 MB"
                }
                self.received_files = [new_file] + self.received_files

                self.status_message = f"Received new file: {new_file['filename']}"
                self.show_status = True
                self.status_is_error = False

                # Continue polling if still active
                if self.is_polling:
                    # Schedule the next poll after the interval
                    await rx.sleep(self.polling_interval)
                    await self.poll_once()

        except Exception as e:
            self.status_message = f"Error while polling: {str(e)}"
            self.show_status = True
            self.status_is_error = True
            self.is_polling = False

    def close_status(self):
        """Close the status dialog."""
        self.show_status = False

    def download_file(self, filename: str):
        """Download a specific file."""
        try:
            self.status_message = f"Downloaded {filename} to {self.download_dir}"
            self.show_status = True
            self.status_is_error = False
        except Exception as e:
            self.status_message = f"Error downloading file: {str(e)}"
            self.show_status = True
            self.status_is_error = True


def receiver():
    """Receiver page for downloading files."""
    return rx.container(
        rx.vstack(
            rx.heading("UUDEX File Transfer - Receiver", size="3"),
            rx.link("Switch to Sender",
                    href="/",
                    button=True,
                    variant="outline"),
            rx.divider(),

            # Status notification if show_status is True
            rx.cond(
                ReceiverState.show_status,
                rx.box(
                    rx.hstack(
                        rx.icon(
                            "check_circle",
                            color=rx.cond(ReceiverState.status_is_error,
                                          "red.500", "green.500"),
                            font_size="xl",
                        ),
                        rx.text(ReceiverState.status_message),
                        rx.spacer(),
                        rx.icon(
                            "close",
                            cursor="pointer",
                            on_click=ReceiverState.close_status,
                            color="gray.500",
                        ),
                        width="100%",
                    ),
                    padding="3",
                    bg=rx.cond(ReceiverState.status_is_error, "red.50",
                               "green.50"),
                    border="1px solid",
                    border_color=rx.cond(ReceiverState.status_is_error,
                                         "red.100", "green.100"),
                    border_radius="md",
                    margin_bottom="4",
                ),
            ),

            # Entity selection
            rx.box(
                rx.vstack(
                    rx.text("Select your entity to receive files:"),
                    rx.select(
                        CertificateState.available_entities,
                        placeholder="Select receiving entity",
                        on_change=ReceiverState.set_entity,
                        value=ReceiverState.entity_name,
                        width="100%",
                    ),
                    align_items="start",
                    spacing="2",
                ),
                width="100%",
                padding="4",
                border="1px solid",
                border_color="gray.200",
                border_radius="md",
                margin_y="4",
            ),

            # Control buttons
            rx.hstack(
                rx.button(
                    "Start Listening",
                    on_click=ReceiverState.start_polling,
                    is_disabled=(ReceiverState.is_polling) |
                    (ReceiverState.entity_name == ""),
                    color_scheme="green",
                ),
                rx.button(
                    "Stop Listening",
                    on_click=ReceiverState.stop_polling,
                    is_disabled=~(ReceiverState.is_polling),
                    color_scheme="red",
                ),
                rx.cond(ReceiverState.is_polling,
                        rx.badge(
                            "Listening...",
                            color_scheme="green",
                        ), rx.badge(
                            "Idle",
                            color_scheme="gray",
                        )),
                width="100%",
                justify="start",
            ),
            rx.divider(margin_y="6"),
            rx.heading("Received Files", size="5"),

            # Files list - using received_files.to() to specify the type
            rx.box(
                rx.cond(
                    ReceiverState.received_files.to(List[Dict[str,
                                                              str]]).length()
                    > 0,
                    rx.vstack(
                        rx.foreach(
                            ReceiverState.received_files.to(List[Dict[str,
                                                                      str]]),
                            lambda file, idx: rx.hstack(
                                rx.vstack(
                                    rx.heading(file["filename"], size="7"),
                                    rx.text(
                                        f"Sent by: {file['sender']} • {file['received']} • {file['size']}",
                                        color="gray.500",
                                        font_size="sm"),
                                    align_items="start",
                                ),
                                rx.spacer(),
                                rx.button(
                                    "Download",
                                    on_click=ReceiverState.download_file(file[
                                        "filename"]),
                                    color_scheme="blue",
                                    size="1",
                                ),
                                width="100%",
                                padding="3",
                                border_bottom="1px solid",
                                border_color="gray.200",
                            )),
                        width="100%",
                        align_items="stretch",
                    ),
                    rx.box(
                        rx.text(
                            "No files received yet. Start listening to receive files.",
                            color="gray.500"),
                        padding="4",
                        text_align="center",
                        width="100%",
                    ),
                ),
                width="100%",
                border="1px solid",
                border_color="gray.200",
                border_radius="md",
                padding="2",
            ),
            rx.box(
                rx.text(
                    f"Saving downloaded files to: {ReceiverState.download_dir}",
                    color="gray.500",
                    font_size="xs"),
                margin_top="6",
                width="100%",
            ),
            spacing="4",
            width="100%",
            padding="20px",
        ),
        max_width="1000px",
        padding="20px",
    )
