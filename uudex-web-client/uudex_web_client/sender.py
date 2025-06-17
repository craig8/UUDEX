import reflex as rx
import os
from typing import List
from .certificate_state import CertificateState


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

    def set_sender_and_determine_recipient(self, sender: str):
        """Set the sender entity and determine the recipient based on the sender."""
        self.sender_entity = sender

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
            # We cannot directly iterate over CertificateState.available_entities
            # So instead, let's select the first entity that's not the sender
            # We'll use a different approach without iteration

            # For now, just pick a default recipient if no mapping exists
            # In a real implementation, you'd want to query the available entities from the backend

            # As a fallback approach, we can use some predefined entities
            available = ["Entity A", "Entity B", "Entity C", "Entity D"]
            filtered = [entity for entity in available if entity != sender]
            if filtered:
                self.recipient_entity = filtered[0]
            else:
                self.recipient_entity = ""

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
            # This would be your actual API call with the uudex_api_client
            # The certificate path for the sender can be retrieved using:
            sender_cert_path = CertificateState.entity_cert_mapping.get(
                self.sender_entity)

            # client = uudex_api_client.Client(sender_cert_path)
            # response = client.send_file(self.recipient_entity, self.file_path)

            # For debugging purposes, print the certificate path
            print(f"Using certificate: {sender_cert_path}")

            # Simulating API call for demonstration
            await rx.sleep(2)  # Simulate network delay

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
    return rx.container(
        rx.vstack(
            rx.heading("UUDEX File Transfer - Sender", size="3"),
            rx.link("Switch to Receiver",
                    href="/receiver",
                    button=True,
                    variant="outline"),
            rx.divider(),

            # Status notification if show_status is True
            rx.cond(
                SenderState.show_status,
                rx.box(
                    rx.hstack(
                        rx.icon(
                            "check_circle",
                            color=rx.cond(SenderState.status_is_error,
                                          "red.500", "green.500"),
                            font_size="xl",
                        ),
                        rx.text(SenderState.status_message),
                        rx.spacer(),
                        rx.icon(
                            "close",
                            cursor="pointer",
                            on_click=SenderState.close_status,
                            color="gray.500",
                        ),
                        width="100%",
                    ),
                    padding="3",
                    bg=rx.cond(SenderState.status_is_error, "red.50",
                               "green.50"),
                    border="1px solid",
                    border_color=rx.cond(SenderState.status_is_error,
                                         "red.100", "green.100"),
                    border_radius="md",
                    margin_bottom="4",
                ),
            ),
            rx.hstack(
                rx.select(
                    CertificateState.available_entities,
                    placeholder="Select sender entity",
                    on_change=SenderState.set_sender_and_determine_recipient,
                    value=SenderState.sender_entity,
                    width="100%",
                ),
                rx.select(
                    CertificateState.available_entities,
                    placeholder="Recipient entity (auto-selected)",
                    value=SenderState.recipient_entity,
                    is_disabled=True,
                    width="100%",
                ),
                width="100%",
                spacing="4",
            ),

            # Simple file input
            rx.box(
                rx.vstack(
                    rx.text("Select a file to transfer:"),
                    rx.input(
                        type="file",
                        on_change=lambda e: SenderState.handle_file_select(e),
                        accept=".csv,.pdf,.txt,.dat",
                    ),
                    rx.text(
                        rx.cond(
                            SenderState.selected_file_name != "",
                            f"Selected file: {SenderState.selected_file_name}",
                            "No file selected"),
                        color=rx.cond(SenderState.selected_file_name != "",
                                      "green.500", "gray.500"),
                        font_size="sm",
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
            rx.button(
                "Send File",
                on_click=SenderState.send_file,
                is_loading=SenderState.is_loading,
                color_scheme="green",
                width="100%",
                is_disabled=rx.cond((SenderState.selected_file_name == "") |
                                    (SenderState.sender_entity == "") |
                                    (SenderState.recipient_entity == ""), True,
                                    False),
            ),
            rx.divider(margin_y="6"),
            rx.heading("Recent Transfers", size="5"),

            # Using HTML table directly
            rx.html("""
                <table width="100%" style="border-collapse: collapse; margin-top: 1rem;">
                    <thead>
                        <tr style="border-bottom: 1px solid #E2E8F0; text-align: left;">
                            <th style="padding: 0.5rem;">File</th>
                            <th style="padding: 0.5rem;">From</th>
                            <th style="padding: 0.5rem;">To</th>
                            <th style="padding: 0.5rem;">Status</th>
                            <th style="padding: 0.5rem;">Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 0.5rem;">example.pdf</td>
                            <td style="padding: 0.5rem;">Entity A</td>
                            <td style="padding: 0.5rem;">Entity B</td>
                            <td style="padding: 0.5rem;">Completed</td>
                            <td style="padding: 0.5rem;">2023-05-10 14:32</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 0.5rem;">data.csv</td>
                            <td style="padding: 0.5rem;">Entity B</td>
                            <td style="padding: 0.5rem;">Entity C</td>
                            <td style="padding: 0.5rem;">Pending</td>
                            <td style="padding: 0.5rem;">2023-05-10 14:30</td>
                        </tr>
                    </tbody>
                </table>
            """),
            rx.box(
                rx.text(
                    f"Using certificate directory: {CertificateState.certs_dir}",
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
