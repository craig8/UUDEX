import reflex as rx
import os
import asyncio
from typing import List, Optional, Dict, Any
from .certificate_state import CertificateState
from .config import uudex_config
import ssl
# Import the uudex api client
from uudex_api_client import AuthenticatedClient
from uudex_api_client.api.endpoints import get_endpoint_user
# from uudex_api_client import AuthenticatedClient, Client, models
# from uudex_api_client.api.endpoints import get_endpoint_user


class SenderState(rx.State):
    """State for the file sender page."""

    # State variables
    sender_entity: str = ""
    recipient_entity: str = ""
    selected_file_name: str = ""
    file_path: str = ""
    status_message: str = ""
    is_loading: bool = False
    show_status: bool = False
    status_is_error: bool = False
    cert_path: str = ""
    key_path: str = ""
    ca_path: str = ""

    # Store the endpoint information returned by get_endpoint_user
    endpoint_data: Dict[str, Any] = {}

    async def set_sender_and_determine_recipient(self, sender: str):
        """
        Set the sender entity and determine the recipient based on the sender.
        Makes an API call to get_endpoint_user to fetch endpoint information.
        """
        self.sender_entity = sender

        cert_state = await self.get_state(CertificateState)

        try:
            # Get certificate path using the CertificateState
            # We need to access the state differently since these are event callbacks
            cert_state = await self.get_state(CertificateState)

            # Use the mapping directly instead of calling event methods
            self.cert_path = cert_state.entity_cert_mapping.get(sender, "")
            self.key_path = self.cert_path.replace(
                '.crt', '.key') if self.cert_path else ""
            self.ca_path = cert_state.ca_cert_path

            # Now we can check if cert_path was found
            if not self.cert_path:
                self.status_message = f"No certificate found for {sender}"
                self.show_status = True
                self.status_is_error = True
                return

            # In a real implementation:
            # Create an authenticated client using the sender's certificate
            # auth_client = cert_state.build_client(entity_name=sender)

            # Get endpoint information
            # endpoint = await get_endpoint_user.asyncio(client=auth_client)

            # Store the endpoint data for later use
            # self.endpoint_data = endpoint.dict() if endpoint else {}

            # For demonstration, we'll simulate getting endpoint data
            await asyncio.sleep(1)  # Simulate API call
            self.endpoint_data = {
                "endpoint_uuid": f"uuid-{sender}",
                "endpoint_user_name": sender,
                "certificate_dn": f"CN={sender}, O=UUDEX",
                "participant_id": 123,
                "description": f"Endpoint for {sender}",
            }

            # Print for debugging
            print(f"Got endpoint data for {sender}: {self.endpoint_data}")

            # Logic to determine recipient based on sender
            sender_recipient_mapping = {
                "Entity A": "Entity B",
                "Entity B": "Entity C",
                "Entity C": "Entity D",
                "Entity D": "Entity A",
            }

            if sender in sender_recipient_mapping:
                self.recipient_entity = sender_recipient_mapping[sender]
            else:
                # Fallback approach
                available = ["Entity A", "Entity B", "Entity C", "Entity D"]
                filtered = [entity for entity in available if entity != sender]
                if filtered:
                    self.recipient_entity = filtered[0]
                else:
                    self.recipient_entity = ""

        except Exception as e:
            self.status_message = f"Error fetching endpoint data: {str(e)}"
            self.show_status = True
            self.status_is_error = True

    async def get_cert_path_for_sender(self, sender: str):
        """
        Helper function to safely get certificate path for a sender.
        """
        # We can't directly access the dictionary in CertificateState from here
        # So let's create a mapping manually based on our knowledge
        # In a real application, you'd want a backend API to provide this information

        # Simulated mapping
        cert_mapping = {
            "Entity A": "/path/to/entityA.crt",
            "Entity B": "/path/to/entityB.crt",
            "Entity C": "/path/to/entityC.crt",
            "Entity D": "/path/to/entityD.crt",
            "uudex-demo.pnl.gov": "/path/to/uudex-demo.crt"
        }

        # Get the certificate path from our mapping
        self.cert_path = cert_mapping.get(sender, "")
        print(f"Got cert path for {sender}: {self.cert_path}")

    def handle_file_select(self, file_name: str):
        """Handle file selection."""
        self.selected_file_name = file_name
        self.file_path = os.path.join("uploads", file_name)

    async def send_file(self):
        """Send the file using the uudex_api_client."""
        if not self.sender_entity or not self.recipient_entity or not self.selected_file_name:
            self.status_message = "Please fill in all fields and select a file."
            self.show_status = True
            self.status_is_error = True
            return

        self.is_loading = True

        try:
            # We'll use the cert_path we've already stored
            if not self.cert_path:
                self.status_message = f"No certificate found for {self.sender_entity}"
                self.show_status = True
                self.status_is_error = True
                self.is_loading = False
                return

            # We can use endpoint data to create a more specific client
            endpoint_uuid = self.endpoint_data.get("endpoint_uuid", "")
            participant_id = self.endpoint_data.get("participant_id", "")

            print(f"Sending file using certificate: {self.cert_path}")
            print(
                f"Endpoint UUID: {endpoint_uuid}, Participant ID: {participant_id}"
            )

            # client = AuthenticatedClient(
            #     base_url="https://your-uudex-server.com",
            #     token=self.get_token_from_cert(self.cert_path),
            # )
            # response = client.send_file(self.recipient_entity, self.file_path)

            # Simulating API call for demonstration
            await asyncio.sleep(2)  # Simulate network delay

            self.status_message = f"File successfully sent from {self.sender_entity} to {self.recipient_entity}!"
            self.status_is_error = False

        except Exception as e:
            self.status_message = f"Error sending file: {str(e)}"
            self.status_is_error = True

        finally:
            self.is_loading = False
            self.show_status = True

    def close_status(self):
        """Close the status dialog."""
        self.show_status = False


def sender():
    """Sender page for uploading files."""
    return rx.box(
        # Header with gradient background
        rx.box(
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "send",
                            size=32,
                            color="white",
                        ),
                        rx.vstack(
                            rx.heading("UUDEX File Transfer",
                                       size="8",
                                       color="white",
                                       font_weight="bold"),
                            rx.text("Secure File Sender",
                                    color="rgba(255,255,255,0.9)",
                                    font_size="lg"),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.link(rx.button(
                                rx.icon("home", size=18, margin_right="8px"),
                                "Home",
                                variant="outline",
                                color_scheme="gray",
                                size="2",
                            ),
                                    href="/"),
                            rx.link(rx.button(
                                rx.icon("download",
                                        size=18,
                                        margin_right="8px"),
                                "Switch to Receiver",
                                variant="outline",
                                color_scheme="gray",
                                size="2",
                            ),
                                    href="/receiver"),
                            spacing="2",
                        ),
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
                    SenderState.show_status,
                    rx.box(
                        rx.hstack(
                            rx.icon(
                                rx.cond(SenderState.status_is_error,
                                        "alert_circle", "check_circle_2"),
                                size=20,
                                color=rx.cond(SenderState.status_is_error,
                                              "red.500", "green.500"),
                            ),
                            rx.text(
                                SenderState.status_message,
                                font_weight="medium",
                                color=rx.cond(SenderState.status_is_error,
                                              "red.700", "green.700"),
                            ),
                            rx.spacer(),
                            rx.icon(
                                "x",
                                size=18,
                                cursor="pointer",
                                on_click=SenderState.close_status,
                                color="gray.400",
                                _hover={"color": "gray.600"},
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        padding="4",
                        bg=rx.cond(SenderState.status_is_error, "red.50",
                                   "green.50"),
                        border="1px solid",
                        border_color=rx.cond(SenderState.status_is_error,
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
                            rx.icon("users", size=20, color="blue.500"),
                            rx.heading("Entity Selection",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Sender Entity",
                                        font_weight="medium",
                                        color="gray.600",
                                        font_size="sm"),
                                rx.select(
                                    CertificateState.available_entities,
                                    placeholder="Select sender entity",
                                    on_change=SenderState.
                                    set_sender_and_determine_recipient,
                                    value=SenderState.sender_entity,
                                    width="100%",
                                    size="2",
                                ),
                                align_items="start",
                                spacing="2",
                                flex="1",
                            ),
                            rx.vstack(
                                rx.text("Recipient Entity",
                                        font_weight="medium",
                                        color="gray.600",
                                        font_size="sm"),
                                rx.select(
                                    CertificateState.available_entities,
                                    placeholder="Auto-selected recipient",
                                    value=SenderState.recipient_entity,
                                    is_disabled=True,
                                    width="100%",
                                    size="2",
                                ),
                                align_items="start",
                                spacing="2",
                                flex="1",
                            ),
                            width="100%",
                            spacing="6",
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

                # Endpoint details card with improved styling
                rx.cond(
                    SenderState.endpoint_data != {},
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("server", size=20, color="blue.500"),
                                rx.heading("Endpoint Details",
                                           size="6",
                                           color="gray.700"),
                                align_items="center",
                                spacing="2",
                            ),
                            rx.divider(color="gray.200"),
                            rx.grid(
                                rx.box(
                                    rx.text("Username",
                                            font_weight="medium",
                                            color="gray.600",
                                            font_size="sm"),
                                    rx.text(SenderState.endpoint_data.get(
                                        'endpoint_user_name', 'N/A'),
                                            font_size="md",
                                            color="gray.800"),
                                    spacing="1",
                                ),
                                rx.box(
                                    rx.text("Participant ID",
                                            font_weight="medium",
                                            color="gray.600",
                                            font_size="sm"),
                                    rx.text(SenderState.endpoint_data.get(
                                        'participant_id', 'N/A'),
                                            font_size="md",
                                            color="gray.800"),
                                    spacing="1",
                                ),
                                rx.box(
                                    rx.text("UUID",
                                            font_weight="medium",
                                            color="gray.600",
                                            font_size="sm"),
                                    rx.text(SenderState.endpoint_data.get(
                                        'endpoint_uuid', 'N/A'),
                                            font_size="sm",
                                            color="gray.600",
                                            font_family="mono"),
                                    spacing="1",
                                ),
                                rx.box(
                                    rx.text("Certificate DN",
                                            font_weight="medium",
                                            color="gray.600",
                                            font_size="sm"),
                                    rx.text(SenderState.endpoint_data.get(
                                        'certificate_dn', 'N/A'),
                                            font_size="sm",
                                            color="gray.600",
                                            font_family="mono"),
                                    spacing="1",
                                ),
                                columns="2",
                                gap="4",
                                width="100%",
                            ),
                            align_items="start",
                            spacing="4",
                        ),
                        background="white",
                        border="1px solid",
                        border_color="blue.200",
                        border_radius="xl",
                        padding="6",
                        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                        margin_bottom="6",
                    ),
                ),

                # File selection card
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("file_up", size=20, color="green.500"),
                            rx.heading("File Selection",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.vstack(
                            rx.text("Select a file to transfer:",
                                    font_weight="medium",
                                    color="gray.600"),
                            rx.box(
                                rx.input(
                                    type="file",
                                    on_change=lambda e: SenderState.
                                    handle_file_select(e),
                                    accept=
                                    ".csv,.pdf,.txt,.dat,.xlsx,.docx,.zip",
                                    width="100%",
                                ),
                                border="2px dashed",
                                border_color="gray.300",
                                border_radius="lg",
                                padding="4",
                                _hover={"border_color": "green.400"},
                                transition="border-color 0.2s",
                            ),
                            rx.hstack(
                                rx.cond(
                                    SenderState.selected_file_name != "",
                                    rx.hstack(
                                        rx.icon("check_circle",
                                                size=16,
                                                color="green.500"),
                                        rx.text(
                                            f"Selected: {SenderState.selected_file_name}",
                                            color="green.600",
                                            font_weight="medium"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    rx.hstack(
                                        rx.icon("file",
                                                size=16,
                                                color="gray.400"),
                                        rx.text("No file selected",
                                                color="gray.500"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                ),
                                justify="start",
                                width="100%",
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

                # Send button with improved styling
                rx.button(
                    rx.cond(
                        SenderState.is_loading,
                        rx.hstack(
                            rx.spinner(size="1", color="white"),
                            rx.text("Sending..."),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.icon("send", size=18),
                            rx.text("Send File"),
                            align_items="center",
                            spacing="2",
                        ),
                    ),
                    on_click=SenderState.send_file,
                    is_loading=SenderState.is_loading,
                    color_scheme="green",
                    size="3",
                    width="100%",
                    height="12",
                    border_radius="lg",
                    font_weight="semibold",
                    is_disabled=rx.cond((SenderState.selected_file_name == "")
                                        | (SenderState.sender_entity == "") |
                                        (SenderState.recipient_entity == ""),
                                        True, False),
                    box_shadow="0 4px 12px rgba(34, 197, 94, 0.3)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 6px 16px rgba(34, 197, 94, 0.4)"
                    },
                    transition="all 0.2s",
                ),

                # Recent transfers section
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("clock", size=20, color="purple.500"),
                            rx.heading("Recent Transfers",
                                       size="6",
                                       color="gray.700"),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.divider(color="gray.200"),
                        rx.box(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell(
                                            "File",
                                            color="gray.600",
                                            font_weight="semibold"),
                                        rx.table.column_header_cell(
                                            "From",
                                            color="gray.600",
                                            font_weight="semibold"),
                                        rx.table.column_header_cell(
                                            "To",
                                            color="gray.600",
                                            font_weight="semibold"),
                                        rx.table.column_header_cell(
                                            "Status",
                                            color="gray.600",
                                            font_weight="semibold"),
                                        rx.table.column_header_cell(
                                            "Time",
                                            color="gray.600",
                                            font_weight="semibold"),
                                    ), ),
                                rx.table.body(
                                    rx.table.row(
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.icon("file_text",
                                                        size=16,
                                                        color="blue.500"),
                                                rx.text("example.pdf",
                                                        font_weight="medium"),
                                                align_items="center",
                                                spacing="2",
                                            )),
                                        rx.table.cell(
                                            rx.text("Entity A",
                                                    color="gray.600")),
                                        rx.table.cell(
                                            rx.text("Entity B",
                                                    color="gray.600")),
                                        rx.table.cell(
                                            rx.badge("Completed",
                                                     color_scheme="green",
                                                     variant="soft")),
                                        rx.table.cell(
                                            rx.text("2023-05-10 14:32",
                                                    color="gray.500",
                                                    font_size="sm")),
                                    ),
                                    rx.table.row(
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.icon("file_spreadsheet",
                                                        size=16,
                                                        color="green.500"),
                                                rx.text("data.csv",
                                                        font_weight="medium"),
                                                align_items="center",
                                                spacing="2",
                                            )),
                                        rx.table.cell(
                                            rx.text("Entity B",
                                                    color="gray.600")),
                                        rx.table.cell(
                                            rx.text("Entity C",
                                                    color="gray.600")),
                                        rx.table.cell(
                                            rx.badge("Pending",
                                                     color_scheme="yellow",
                                                     variant="soft")),
                                        rx.table.cell(
                                            rx.text("2023-05-10 14:30",
                                                    color="gray.500",
                                                    font_size="sm")),
                                    ),
                                ),
                                variant="surface",
                                size="2",
                            ),
                            width="100%",
                            overflow_x="auto",
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
                            f"Certificate directory: {CertificateState.certs_dir}",
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
