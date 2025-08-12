import reflex as rx
import os
import time
import asyncio
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
            await asyncio.sleep(2)  # Simulate network delay

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
                    await asyncio.sleep(self.polling_interval)
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
    return rx.box(
        # Header with gradient background
        rx.box(
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "download",
                            size=32,
                            color="white",
                        ),
                        rx.vstack(
                            rx.heading("UUDEX File Transfer",
                                       size="8",
                                       color="white",
                                       font_weight="bold"),
                            rx.text("Secure File Receiver",
                                    color="rgba(255,255,255,0.9)",
                                    font_size="lg"),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.link(rx.button(
                            rx.icon("send", size=18, margin_right="8px"),
                            "Switch to Sender",
                            variant="outline",
                            color_scheme="gray",
                            size="2",
                        ),
                                href="/"),
                        align_items="center",
                        width="100%",
                    ),
                    spacing="6",
                    padding_y="8",
                ),
                max_width="1200px",
            ),
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            width="100%",
            box_shadow="0 4px 20px rgba(0,0,0,0.1)",
        ),

        # Main content
        rx.container(
            rx.vstack(
                # Status notification with improved styling
                rx.cond(
                    ReceiverState.show_status,
                    rx.box(
                        rx.hstack(
                            rx.icon(
                                rx.cond(ReceiverState.status_is_error,
                                        "alert_circle", "check_circle_2"),
                                size=20,
                                color=rx.cond(ReceiverState.status_is_error,
                                              "red.500", "green.500"),
                            ),
                            rx.text(
                                ReceiverState.status_message,
                                font_weight="medium",
                                color=rx.cond(ReceiverState.status_is_error,
                                              "red.700", "green.700"),
                            ),
                            rx.spacer(),
                            rx.icon(
                                "x",
                                size=18,
                                cursor="pointer",
                                on_click=ReceiverState.close_status,
                                color="gray.400",
                                _hover={"color": "gray.600"},
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        padding="4",
                        bg=rx.cond(ReceiverState.status_is_error, "red.50",
                                   "green.50"),
                        border="1px solid",
                        border_color=rx.cond(ReceiverState.status_is_error,
                                             "red.200", "green.200"),
                        border_radius="lg",
                        margin_bottom="6",
                        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                    ),
                ),

                # Entity selection card
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("user", size=20, color="blue.500"),
                            rx.heading("Entity Selection",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.vstack(
                            rx.text("Select your entity to receive files:",
                                    font_weight="medium",
                                    color="gray.600"),
                            rx.select(
                                CertificateState.available_entities,
                                placeholder="Select receiving entity",
                                on_change=ReceiverState.set_entity,
                                value=ReceiverState.entity_name,
                                width="100%",
                                size="2",
                            ),
                            align_items="start",
                            spacing="3",
                            width="100%",
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    background="white",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="xl",
                    padding="6",
                    box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                    margin_bottom="6",
                ),

                # Control panel card
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("radio", size=20, color="green.500"),
                            rx.heading("Listening Control",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("play", size=16),
                                    rx.text("Start Listening"),
                                    align_items="center",
                                    spacing="2",
                                ),
                                on_click=ReceiverState.start_polling,
                                is_disabled=(ReceiverState.is_polling) |
                                (ReceiverState.entity_name == ""),
                                color_scheme="green",
                                size="2",
                                border_radius="lg",
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon("stop", size=16),
                                    rx.text("Stop Listening"),
                                    align_items="center",
                                    spacing="2",
                                ),
                                on_click=ReceiverState.stop_polling,
                                is_disabled=~(ReceiverState.is_polling),
                                color_scheme="red",
                                size="2",
                                border_radius="lg",
                            ),
                            rx.spacer(),
                            rx.cond(
                                ReceiverState.is_polling,
                                rx.hstack(
                                    rx.spinner(size="1", color="green.500"),
                                    rx.badge(
                                        "Listening for files...",
                                        color_scheme="green",
                                        variant="soft",
                                        size="2",
                                    ),
                                    align_items="center",
                                    spacing="2",
                                ),
                                rx.badge(
                                    "Idle",
                                    color_scheme="gray",
                                    variant="soft",
                                    size="2",
                                ),
                            ),
                            width="100%",
                            align_items="center",
                            spacing="4",
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    background="white",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="xl",
                    padding="6",
                    box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                    margin_bottom="6",
                ),
                # Received files section
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("inbox", size=20, color="purple.500"),
                            rx.heading("Received Files",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.cond(
                            ReceiverState.received_files.to(
                                List[Dict[str, str]]).length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    ReceiverState.received_files.to(
                                        List[Dict[str, str]]),
                                    lambda file, idx: rx.box(
                                        rx.hstack(
                                            rx.icon("file",
                                                    size=24,
                                                    color="blue.500"),
                                            rx.vstack(
                                                rx.text(file["filename"],
                                                        font_weight="bold",
                                                        font_size="lg",
                                                        color="gray.800"),
                                                rx.hstack(
                                                    rx.text(
                                                        f"From: {file['sender']}",
                                                        color="gray.600",
                                                        font_size="sm"),
                                                    rx.text("•",
                                                            color="gray.400",
                                                            font_size="sm"),
                                                    rx.text(file["received"],
                                                            color="gray.600",
                                                            font_size="sm"),
                                                    rx.text("•",
                                                            color="gray.400",
                                                            font_size="sm"),
                                                    rx.text(file["size"],
                                                            color="gray.600",
                                                            font_size="sm"),
                                                    spacing="2",
                                                ),
                                                align_items="start",
                                                spacing="1",
                                            ),
                                            rx.spacer(),
                                            rx.button(
                                                rx.hstack(
                                                    rx.icon("download",
                                                            size=16),
                                                    rx.text("Download"),
                                                    align_items="center",
                                                    spacing="2",
                                                ),
                                                on_click=ReceiverState.
                                                download_file(file["filename"]
                                                              ),
                                                color_scheme="blue",
                                                size="2",
                                                border_radius="lg",
                                                box_shadow=
                                                "0 2px 8px rgba(59, 130, 246, 0.2)",
                                                _hover={
                                                    "transform":
                                                    "translateY(-1px)",
                                                    "box_shadow":
                                                    "0 4px 12px rgba(59, 130, 246, 0.3)"
                                                },
                                                transition="all 0.2s",
                                            ),
                                            align_items="center",
                                            width="100%",
                                            spacing="4",
                                        ),
                                        padding="4",
                                        border="1px solid",
                                        border_color="gray.200",
                                        border_radius="lg",
                                        background="white",
                                        box_shadow=
                                        "0 1px 3px rgba(0,0,0,0.05)",
                                        _hover={
                                            "border_color":
                                            "blue.300",
                                            "box_shadow":
                                            "0 2px 8px rgba(0,0,0,0.1)"
                                        },
                                        transition="all 0.2s",
                                        margin_bottom="3",
                                    ),
                                ),
                                width="100%",
                                spacing="3",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.icon("inbox", size=48,
                                            color="gray.300"),
                                    rx.text(
                                        "No files received yet",
                                        font_size="xl",
                                        color="gray.500",
                                        font_weight="medium",
                                    ),
                                    rx.text(
                                        "Start listening to receive files from other entities",
                                        color="gray.400",
                                        font_size="sm",
                                        text_align="center",
                                    ),
                                    align_items="center",
                                    spacing="3",
                                ),
                                padding="12",
                                text_align="center",
                                width="100%",
                                background="gray.50",
                                border_radius="lg",
                                border="2px dashed",
                                border_color="gray.200",
                            ),
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    background="white",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="xl",
                    padding="6",
                    box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                    margin_bottom="6",
                ),
                # Footer info
                rx.box(
                    rx.hstack(
                        rx.icon("folder", size=16, color="gray.400"),
                        rx.text(
                            f"Download directory: {ReceiverState.download_dir}",
                            color="gray.500",
                            font_size="sm"),
                        align_items="center",
                        spacing="2",
                    ),
                    width="100%",
                    padding="4",
                    border_top="1px solid",
                    border_color="gray.200",
                    margin_top="6",
                ),
                spacing="6",
                width="100%",
                padding="8",
            ),
            max_width="1200px",
            padding="8",
            margin_top="8",
        ),

        # Background
        background="linear-gradient(to bottom, #f8fafc, #e2e8f0)",
        min_height="100vh",
        width="100%",
    )
