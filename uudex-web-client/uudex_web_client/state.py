# uudex_web_client/state.py
import logging
import reflex as rx
from typing import Any, Dict, List, ClassVar, Optional

from .config import uudex_config
from .services import UudexAPIService
import rxconfig

logger = logging.getLogger(__name__)


class State(rx.State):
    """The app state."""
    # Store list of participants as dictionaries
    participants: List[Dict[str, Any]] = []
    loading: bool = False
    error: str = ""

    # Config settings
    available_certs: List[str] = []
    selected_cert: str = ""
    api_url: str = ""

    # Form data
    participant_uuid: str = ""
    participant_short_name: str = ""
    participant_long_name: str = ""
    root_org_sw: str = "Y"
    description: str = ""

    # Flag to track if the app has been initialized
    initialized: bool = False

    @rx.event
    def on_load(self):
        """Initialize the application."""
        # Set the initialized flag
        self.initialized = True

        # Get available certificates
        self.available_certs = uudex_config.get_available_certs()

        # Set defaults
        if self.available_certs:
            self.selected_cert = self.available_certs[0]
        else:
            # Default to the configured default cert name
            self.selected_cert = uudex_config.DEFAULT_CERT_NAME

        # Set default API URL from config
        self.api_url = uudex_config.get_uudex_url()

        # Trigger loading of participants
        #return rx.event(self.get_participants)

    # Handle settings form submission
    def handle_settings_submit(self, form_data: Dict):
        """Handle settings form submission."""
        # Extract values from form data
        new_api_url = form_data.get("api_url", "")
        new_selected_cert = form_data.get("selected_cert", "")

        # Update state
        if new_api_url:
            self.api_url = new_api_url
        if new_selected_cert:
            self.selected_cert = new_selected_cert

        # Log the change
        logger.info(
            f"Updated API config: URL={self.api_url}, Cert={self.selected_cert}"
        )

        # Clear any existing error
        self.error = ""

        # Test the connection with the new settings
        return rx.event(self.get_participants)

    # Handle participant form submission
    def handle_participant_submit(self, form_data: Dict):
        """Handle participant form submission."""
        # Extract values from form data
        self.participant_uuid = form_data.get("participant_uuid", "")
        self.participant_short_name = form_data.get("participant_short_name",
                                                    "")
        self.participant_long_name = form_data.get("participant_long_name", "")
        self.root_org_sw = form_data.get("root_org_sw", "Y")
        self.description = form_data.get("description", "")

        # Create a participant object
        participant_data = {
            "participant_uuid": self.participant_uuid,
            "participant_short_name": self.participant_short_name,
            "participant_long_name": self.participant_long_name,
            "root_org_sw": self.root_org_sw,
            "description": self.description
        }

        # Add the participant
        return rx.event(self._add_participant, participant_data)

    def navigate(self, route: str):
        """Navigate to a given route."""
        return rx.redirect(route)

    def get_api_service(self) -> UudexAPIService:
        """Get or create an API service instance with the current settings."""
        # Get cert path if a cert is selected
        cert_path = None
        if self.selected_cert:
            cert_path = uudex_config.get_cert_path(self.selected_cert)

        # Use the selected URL or fallback to config
        base_url = self.api_url or uudex_config.get_uudex_url()

        # Ensure URL has the correct format with /api prefix
        if not base_url.endswith('/api'):
            if base_url.endswith('/'):
                base_url = f"{base_url}api"
            else:
                base_url = f"{base_url}/api"

        logger.info(
            f"Creating API service with URL: {base_url}, Cert: {self.selected_cert}"
        )
        logger.info(
            f"Debug mode: {uudex_config.DEBUG_MODE}, SSL header bypass: {uudex_config.BYPASS_SSL_HEADER}"
        )

        # Create the API service with the certificate path and debug settings
        return UudexAPIService(
            base_url=base_url,
            cert_path=cert_path,
            verify_ssl=True,
            debug_mode=uudex_config.DEBUG_MODE,
            bypass_ssl_header=uudex_config.BYPASS_SSL_HEADER)

    async def get_participants(self):
        """Fetch all participants from the API."""
        self.loading = True
        self.error = ""

        try:
            # Get API service with current settings
            api_service = self.get_api_service()
            result = await api_service.get_all_participants()

            if result.success:
                self.participants = result.data
                logger.info(f"Loaded {len(self.participants)} participants")
            else:
                self.error = result.error
                logger.error(f"Error fetching participants: {result.error}")

        except Exception as e:
            self.error = f"Unexpected error: {str(e)}"
            logger.exception("Unexpected error in get_participants")

        finally:
            self.loading = False

    async def _add_participant(self, participant_data: Dict[str, Any]):
        """Add a new participant (internal implementation)."""
        self.loading = True
        self.error = ""

        try:
            # Get API service with current settings
            api_service = self.get_api_service()
            result = await api_service.create_participant(participant_data)

            if result.success:
                # Add the new participant to the list
                self.participants.append(result.data)
                logger.info(
                    f"Added new participant: {result.data['participant_short_name']}"
                )

                # Clear form data
                self.participant_uuid = ""
                self.participant_short_name = ""
                self.participant_long_name = ""
                self.root_org_sw = "Y"
                self.description = ""
            else:
                self.error = result.error
                logger.error(f"Error adding participant: {result.error}")

        except Exception as e:
            self.error = f"Unexpected error: {str(e)}"
            logger.exception("Unexpected error in add_participant")

        finally:
            self.loading = False

    async def delete_participant(self, participant_id: str):
        """Delete a participant."""
        self.loading = True
        self.error = ""

        try:
            # Get API service with current settings
            api_service = self.get_api_service()
            result = await api_service.delete_participant(participant_id)

            if result.success:
                # Remove the participant from the list
                self.participants = [
                    p for p in self.participants
                    if p["participant_uuid"] != participant_id
                ]
                logger.info(f"Deleted participant: {participant_id}")
            else:
                self.error = result.error
                logger.error(f"Error deleting participant: {result.error}")

        except Exception as e:
            self.error = f"Unexpected error: {str(e)}"
            logger.exception("Unexpected error in delete_participant")

        finally:
            self.loading = False
