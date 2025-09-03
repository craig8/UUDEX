import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import reflex as rx

# Import UUDEX API client
from uudex_api_client import Client
from uudex_api_client.api.datasets import (
    create_dataset,
    delete_dataset,
    get_all_datasets,
    get_dataset_by_id,
    update_dataset,
)
from uudex_api_client.api.endpoints import (
    create_endpoint,
    delete_endpoint,
    get_all_endpoints,
    get_endpoint_by_id,
    get_endpoint_user,
    update_endpoint,
)
from uudex_api_client.api.participants import (
    create_participant,
    delete_participant,
    get_all_participants,
    get_participant_by_id,
    update_participant,
)
from uudex_api_client.api.subjects import (
    bulk_subject_operations,
    create_subject,
    delete_subject,
    get_all_subjects,
    get_subject_by_id,
    get_subjects_with_metrics,
    update_subject,
)
from uudex_api_client.api.subscriptions import (
    create_subscription,
    delete_subscription,
    get_admin_subscriptions,
    get_subscription_by_uuid,
    get_user_subscriptions,
    update_subscription,
)
from uudex_api_client.models import (
    DatasetCreate,
    DatasetRead,
    EndPoint,
    EndPointCreate,
    EndPointUpdate,
    Participant,
    ParticipantCreate,
    Subject,
    SubjectCreate,
    SubjectUpdate,
    Subscription,
    SubscriptionCreate,
)


from .certificate_state import CertificateState, endpoints
from .config import uudex_config


class AdminState(rx.State):
    """State for the admin panel."""

    # Authentication
    selected_admin_entity: str = ""
    is_authenticated: bool = False
    admin_cert_path: str = ""
    admin_key_path: str = ""
    admin_ca_path: str = ""

    # Admin capabilities
    is_uudex_admin: bool = False
    is_participant_admin: bool = False
    admin_entities: List[Dict[str, Any]] = []  # Entities with admin capabilities
    admin_endpoint_id: Optional[int] = None  # The endpoint ID of the authenticated admin
    admin_participant_id: Optional[int] = None  # The participant ID for participant admins

    # Status and UI state
    status_message: str = ""
    show_status: bool = False
    status_is_error: bool = False
    is_loading: bool = False
    current_section: str = "participants"

    # Data stores
    participants: List[Dict[str, Any]] = []
    subjects: List[Dict[str, Any]] = []
    subscriptions: List[Dict[str, Any]] = []
    endpoints: List[Dict[str, Any]] = []
    datasets: List[Dict[str, Any]] = []

    # Form states for creating/editing
    show_create_participant_form: bool = False
    show_create_subject_form: bool = False
    show_create_subscription_form: bool = False
    show_create_endpoint_form: bool = False
    show_create_dataset_form: bool = False

    # Edit states
    show_edit_participant_form: bool = False
    show_edit_subject_form: bool = False
    show_edit_subscription_form: bool = False
    show_edit_endpoint_form: bool = False
    show_edit_dataset_form: bool = False

    # Current editing IDs
    editing_participant_id: Optional[int] = None
    editing_subject_id: Optional[int] = None
    editing_subscription_id: Optional[int] = None
    editing_endpoint_id: Optional[int] = None
    editing_dataset_id: Optional[int] = None

    # Form data
    participant_form: Dict[str, str] = {
        "participant_short_name": "",
        "participant_long_name": "",
        "description": "",
        "root_org_sw": "N",
        "active_sw": "Y",
        "uudex_administrator_sw": "N",
        "participant_administrator_sw": "N"
    }

    subject_form: Dict[str, Any] = {
        "subject_name": "",
        "dataset_instance_key": "",
        "subscription_type": "PUSH",
        "fulfillment_types_available": "QUEUE",
        "full_queue_behavior": "REJECT",
        "max_queue_size_kb": 1024,
        "max_message_count": 1000,
        "priority": 5,
        "backing_exchange_name": "",
        "owner_participant_id": 0,
        "dataset_definition_id": 1
    }

    subscription_form: Dict[str, Any] = {
        "subscription_name": "",
        "subscription_state": "ACTIVE",
        "owner_endpoint_id": 0
    }

    endpoint_form: Dict[str, str] = {
        "endpoint_user_name": "",
        "certificate_dn": "",
        "participant_id": "0",
        "active_sw": "Y",
        "uudex_administrator_sw": "N",
        "participant_administrator_sw": "N"
    }

    dataset_form: Dict[str, Any] = {
        "dataset_name": "",
        "description": "",
        "properties": "",
        "payload": "",  # Base64 encoded
        "payload_compression_algorithm": "none",
        "version_number": 1,
        "subject_id": 0
    }

    async def load_admin_entities(self):
        """Load entities that have admin capabilities."""
        admin_entities = []
        cert_state = await self.get_state(CertificateState)

        for entity_name in cert_state.available_entities:
            # Get endpoint info from the cached endpoints
            endpoint = endpoints.get_by_username(entity_name)
            if endpoint:
                # Since available_entities is already filtered to admins, just add them
                admin_entities.append({
                    "name": entity_name,
                    "endpoint_user_name": endpoint.user_name or entity_name,
                    "is_uudex_admin": endpoint.uudex_administrator_sw == "Y",
                    "is_participant_admin": endpoint.participant_administrator_sw == "Y",
                    "is_active": endpoint.active_sw == "Y",
                    "participant_id": endpoint.participant_id
                })

        # Sort by endpoint_user_name
        admin_entities.sort(key=lambda x: x["endpoint_user_name"].lower())
        self.admin_entities = admin_entities

    async def authenticate_admin(self, display_name: str):
        """Authenticate as admin using the selected entity display name."""
        self.selected_admin_entity = display_name

        cert_state = await self.get_state(CertificateState)

        # Convert display name to certificate name
        entity = cert_state.display_name_to_cert_name.get(display_name, display_name)

        # Get certificate paths
        self.admin_cert_path = cert_state.entity_cert_mapping.get(entity, "")
        self.admin_key_path = self.admin_cert_path.replace('.crt', '.key') if self.admin_cert_path else ""
        self.admin_ca_path = cert_state.ca_cert_path

        if not self.admin_cert_path:
            self.status_message = f"No certificate found for {display_name}"
            self.show_status = True
            self.status_is_error = True
            self.is_authenticated = False
            return

        # Test authentication by checking if certificates exist and are readable
        try:
            # Simple validation - check if certificate files exist and are readable
            if not Path(self.admin_cert_path).exists():
                raise Exception(f"Certificate file not found: {self.admin_cert_path}")
            if not Path(self.admin_key_path).exists():
                raise Exception(f"Key file not found: {self.admin_key_path}")
            if not Path(self.admin_ca_path).exists():
                raise Exception(f"CA certificate file not found: {self.admin_ca_path}")

            # Call /endpoint/me to get permissions from the server
            client = self._get_admin_client()
            endpoint_result = await get_endpoint_user.asyncio(client=client)
            
            if endpoint_result:
                # Store the endpoint information
                self.admin_endpoint_id = endpoint_result.endpoint_id
                self.admin_participant_id = endpoint_result.participant_id
                
                # Check permissions from the server response
                self.is_uudex_admin = endpoint_result.uudex_administrator_sw == "Y"
                self.is_participant_admin = endpoint_result.participant_administrator_sw == "Y"
                
                if not self.is_uudex_admin and not self.is_participant_admin:
                    self.status_message = f"{display_name} does not have admin privileges"
                    self.show_status = True
                    self.status_is_error = True
                    self.is_authenticated = False
                    return
                
                # Authentication successful
                self.is_authenticated = True
                admin_type = "UUDEX Admin" if self.is_uudex_admin else "Participant Admin"
                self.status_message = f"Successfully authenticated as {display_name} ({admin_type})"
                self.show_status = True
                self.status_is_error = False
                # Load initial data
                await self.load_all_data()
            else:
                # Server returned 401 or another error
                self.status_message = f"Invalid certificate or insufficient permissions for {display_name}"
                self.show_status = True
                self.status_is_error = True
                self.is_authenticated = False

        except Exception as e:
            # Handle authentication errors gracefully
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                self.status_message = f"Invalid certificate or insufficient permissions for {display_name}"
            else:
                self.status_message = f"Authentication failed: {error_msg}"
            self.show_status = True
            self.status_is_error = True
            self.is_authenticated = False

    def _get_admin_client(self) -> Client:
        """Get authenticated client for admin operations."""
        httpx_args = {
            'cert': (self.admin_cert_path, self.admin_key_path),
        }
        return Client(
            base_url="https://localhost",
            verify_ssl=self.admin_ca_path,
            httpx_args=httpx_args
        )

    async def load_all_data(self):
        """Load all admin data."""
        if not self.is_authenticated:
            return

        self.is_loading = True
        try:
            # Load different data based on admin type
            tasks = []
            if self.is_uudex_admin:
                tasks.extend([
                    self.load_participants(),
                    self.load_endpoints(),
                    self.load_subjects(),
                    self.load_subscriptions(),
                    self.load_datasets()
                ])
            elif self.is_participant_admin:
                # Participant admins can see limited data
                tasks.extend([
                    self.load_participants(),  # Will be filtered to their participant only
                    self.load_endpoints(),  # Will be filtered to their participant's endpoints
                    self.load_subjects(),
                    self.load_subscriptions(),
                    self.load_datasets()
                ])

            if tasks:
                await asyncio.gather(*tasks)

            self.status_message = "Data loaded successfully"
            self.show_status = True
            self.status_is_error = False
        except Exception as e:
            self.status_message = f"Error loading data: {str(e)}"
            self.show_status = True
            self.status_is_error = True
        finally:
            self.is_loading = False

    async def load_participants(self):
        """Load all participants."""
        try:
            client = self._get_admin_client()
            result = await get_all_participants.asyncio(client=client)

            if result:
                # Filter participants based on admin type
                if self.is_participant_admin and not self.is_uudex_admin:
                    # Participant admins can only see their own participant
                    filtered_participants = [p.to_dict() for p in result if p.participant_id == self.admin_participant_id]
                else:
                    # UUDEX admins can see all participants
                    filtered_participants = [p.to_dict() for p in result]
                
                # Sort by participant_short_name
                filtered_participants.sort(key=lambda x: x.get("participant_short_name", "").lower())
                self.participants = filtered_participants
            else:
                self.participants = []

        except Exception as e:
            print(f"Error loading participants: {e}")
            self.participants = []

    async def load_subjects(self):
        """Load all subjects."""
        try:
            client = self._get_admin_client()
            result = await get_all_subjects.asyncio(client=client)

            if result:
                subjects_list = [s.to_dict() for s in result]
                # Sort by subject_name
                subjects_list.sort(key=lambda x: x.get("subject_name", "").lower())
                self.subjects = subjects_list
            else:
                self.subjects = []

        except Exception as e:
            print(f"Error loading subjects: {e}")
            self.subjects = []

    async def load_subscriptions(self):
        """Load all subscriptions."""
        try:
            client = self._get_admin_client()
            result = await get_admin_subscriptions.asyncio(client=client)

            if result:
                subscriptions_list = [s.to_dict() for s in result]
                # Sort by subscription_name
                subscriptions_list.sort(key=lambda x: x.get("subscription_name", "").lower())
                self.subscriptions = subscriptions_list
            else:
                self.subscriptions = []

        except Exception as e:
            print(f"Error loading subscriptions: {e}")
            self.subscriptions = []

    async def load_endpoints(self):
        """Load all endpoints."""
        try:
            print(f"[DEBUG] Loading endpoints - is_uudex_admin: {self.is_uudex_admin}, is_participant_admin: {self.is_participant_admin}")
            client = self._get_admin_client()
            result = await get_all_endpoints.asyncio(client=client)
            print(f"[DEBUG] get_all_endpoints returned: {len(result) if result else 0} endpoints")

            if result:
                # Filter endpoints based on admin type
                if self.is_participant_admin and not self.is_uudex_admin:
                    # Participant admins can only see endpoints for their participant
                    filtered_endpoints = [e.to_dict() for e in result if e.participant_id == self.admin_participant_id]
                    print(f"[DEBUG] Participant admin filtered endpoints: {len(filtered_endpoints)} (participant_id: {self.admin_participant_id})")
                else:
                    # UUDEX admins can see all endpoints
                    filtered_endpoints = [e.to_dict() for e in result]
                    print(f"[DEBUG] UUDEX admin - showing all {len(filtered_endpoints)} endpoints")
                
                # Sort by endpoint_user_name
                filtered_endpoints.sort(key=lambda x: x.get("endpoint_user_name", "").lower())
                self.endpoints = filtered_endpoints
                print(f"[DEBUG] Final endpoints list: {[ep.get('endpoint_user_name') for ep in filtered_endpoints]}")
            else:
                print("[DEBUG] No endpoints returned from API")
                self.endpoints = []

        except Exception as e:
            print(f"Error loading endpoints: {e}")
            self.endpoints = []

    async def load_datasets(self):
        """Load all datasets."""
        try:
            client = self._get_admin_client()
            result = await get_all_datasets.asyncio(client=client)

            if result:
                datasets_list = [d.to_dict() for d in result]
                # Sort by dataset_name
                datasets_list.sort(key=lambda x: x.get("dataset_name", "").lower())
                self.datasets = datasets_list
            else:
                self.datasets = []

        except Exception as e:
            print(f"Error loading datasets: {e}")
            self.datasets = []

    def set_section(self, section: str):
        """Set the current admin section."""
        self.current_section = section

    def close_status(self):
        """Close status message."""
        self.show_status = False

    # Participant management
    def show_create_participant(self):
        """Show create participant form."""
        if not self.is_uudex_admin:
            self.status_message = "Only UUDEX Administrators can create participants"
            self.show_status = True
            self.status_is_error = True
            return
        self.show_create_participant_form = True

    def hide_create_participant(self):
        """Hide create participant form."""
        self.show_create_participant_form = False
        # Reset form
        self.participant_form = {
            "participant_short_name": "",
            "participant_long_name": "",
            "description": "",
            "root_org_sw": "N",
            "active_sw": "Y",
            "uudex_administrator_sw": "N",
            "participant_administrator_sw": "N"
        }

    def update_participant_form(self, field: str, value: str):
        """Update participant form field."""
        self.participant_form = {**self.participant_form, field: value}

    async def create_participant_submit(self):
        """Submit new participant."""
        if not self.is_authenticated:
            return
            
        # Only UUDEX admins can create participants
        if not self.is_uudex_admin:
            self.status_message = "Only UUDEX Administrators can create participants"
            self.show_status = True
            self.status_is_error = True
            return

        self.is_loading = True
        try:
            client = self._get_admin_client()
            participant_data = ParticipantCreate(
                participant_short_name=self.participant_form["participant_short_name"],
                participant_long_name=self.participant_form["participant_long_name"],
                description=self.participant_form["description"] or None,
                root_org_sw=self.participant_form["root_org_sw"],
                active_sw=self.participant_form["active_sw"]
            )

            result = await create_participant.asyncio(client=client, body=participant_data)

            if result:
                self.status_message = f"Participant '{result.participant_short_name}' created successfully"
                self.show_status = True
                self.status_is_error = False
                self.hide_create_participant()
                await self.load_participants()
            else:
                raise Exception("Failed to create participant")

        except Exception as e:
            self.status_message = f"Error creating participant: {str(e)}"
            self.show_status = True
            self.status_is_error = True
        finally:
            self.is_loading = False

    # Subject management
    def show_create_subject(self):
        """Show create subject form."""
        self.show_create_subject_form = True

    def hide_create_subject(self):
        """Hide create subject form."""
        self.show_create_subject_form = False

    def update_subject_form(self, field: str, value: Any):
        """Update subject form field."""
        self.subject_form = {**self.subject_form, field: value}

    async def create_subject_submit(self):
        """Submit new subject."""
        if not self.is_authenticated:
            return

        self.is_loading = True
        try:
            client = self._get_admin_client()
            subject_data = SubjectCreate(
                subject_name=self.subject_form["subject_name"],
                dataset_instance_key=self.subject_form["dataset_instance_key"],
                subscription_type=self.subject_form["subscription_type"],
                fulfillment_types_available=self.subject_form["fulfillment_types_available"],
                full_queue_behavior=self.subject_form["full_queue_behavior"],
                max_queue_size_kb=self.subject_form["max_queue_size_kb"],
                max_message_count=self.subject_form["max_message_count"],
                priority=self.subject_form["priority"],
                backing_exchange_name=self.subject_form["backing_exchange_name"],
                owner_participant_id=self.subject_form["owner_participant_id"],
                dataset_definition_id=self.subject_form["dataset_definition_id"]
            )

            result = await create_subject.asyncio(client=client, body=subject_data)

            if result:
                self.status_message = f"Subject '{result.subject_name}' created successfully"
                self.show_status = True
                self.status_is_error = False
                self.hide_create_subject()
                await self.load_subjects()
            else:
                raise Exception("Failed to create subject")

        except Exception as e:
            self.status_message = f"Error creating subject: {str(e)}"
            self.show_status = True
            self.status_is_error = True
        finally:
            self.is_loading = False

    # Subscription management
    def show_create_subscription(self):
        """Show create subscription form."""
        self.show_create_subscription_form = True

    def hide_create_subscription(self):
        """Hide create subscription form."""
        self.show_create_subscription_form = False

    def update_subscription_form(self, field: str, value: Any):
        """Update subscription form field."""
        self.subscription_form = {**self.subscription_form, field: value}

    async def create_subscription_submit(self):
        """Submit new subscription."""
        if not self.is_authenticated:
            return

        self.is_loading = True
        try:
            client = self._get_admin_client()
            subscription_data = SubscriptionCreate(
                subscription_name=self.subscription_form["subscription_name"],
                subscription_state=self.subscription_form["subscription_state"],
                owner_endpoint_id=self.subscription_form["owner_endpoint_id"]
            )

            result = await create_subscription.asyncio(client=client, body=subscription_data)

            if result:
                self.status_message = f"Subscription '{result.subscription_name}' created successfully"
                self.show_status = True
                self.status_is_error = False
                self.hide_create_subscription()
                await self.load_subscriptions()
            else:
                raise Exception("Failed to create subscription")

        except Exception as e:
            self.status_message = f"Error creating subscription: {str(e)}"
            self.show_status = True
            self.status_is_error = True
        finally:
            self.is_loading = False

    # Endpoint management
    def show_create_endpoint(self):
        """Show create endpoint form."""
        if not self.is_uudex_admin and not self.is_participant_admin:
            self.status_message = "Admin privileges required to create endpoints"
            self.show_status = True
            self.status_is_error = True
            return
        
        # If participant admin, pre-fill the participant_id
        if self.is_participant_admin and not self.is_uudex_admin:
            self.endpoint_form["participant_id"] = str(self.admin_participant_id)
        
        self.show_create_endpoint_form = True

    def hide_create_endpoint(self):
        """Hide create endpoint form."""
        self.show_create_endpoint_form = False
        # Reset form
        self.endpoint_form = {
            "endpoint_user_name": "",
            "certificate_dn": "",
            "participant_id": "0",
            "active_sw": "Y",
            "uudex_administrator_sw": "N",
            "participant_administrator_sw": "N"
        }

    def update_endpoint_form(self, field: str, value: str):
        """Update endpoint form field."""
        self.endpoint_form = {**self.endpoint_form, field: value}

    async def create_endpoint_submit(self):
        """Submit new endpoint."""
        if not self.is_authenticated:
            return

        # Check permissions
        if not self.is_uudex_admin and not self.is_participant_admin:
            self.status_message = "Admin privileges required to create endpoints"
            self.show_status = True
            self.status_is_error = True
            return

        self.is_loading = True
        try:
            # Participant admins can only create endpoints for their own participant
            if self.is_participant_admin and not self.is_uudex_admin:
                # Force the participant_id to be their own
                self.endpoint_form["participant_id"] = str(self.admin_participant_id)
                # Participant admins cannot create admin endpoints
                self.endpoint_form["uudex_administrator_sw"] = "N"
                self.endpoint_form["participant_administrator_sw"] = "N"

            client = self._get_admin_client()
            endpoint_data = EndPointCreate(
                endpoint_user_name=self.endpoint_form["endpoint_user_name"],
                certificate_dn=self.endpoint_form["certificate_dn"],
                participant_id=int(self.endpoint_form["participant_id"]),
                active_sw=self.endpoint_form["active_sw"],
                uudex_administrator_sw=self.endpoint_form["uudex_administrator_sw"],
                participant_administrator_sw=self.endpoint_form["participant_administrator_sw"]
            )

            result = await create_endpoint.asyncio(client=client, body=endpoint_data)

            if result:
                self.status_message = f"Endpoint '{result.endpoint_user_name}' created successfully"
                self.show_status = True
                self.status_is_error = False
                self.hide_create_endpoint()
                await self.load_endpoints()
            else:
                raise Exception("Failed to create endpoint")

        except Exception as e:
            self.status_message = f"Error creating endpoint: {str(e)}"
            self.show_status = True
            self.status_is_error = True
        finally:
            self.is_loading = False

    # Dataset management methods
    def show_create_dataset(self):
        """Show create dataset form."""
        self.show_create_dataset_form = True

    def hide_create_dataset(self):
        """Hide create dataset form."""
        self.show_create_dataset_form = False


def admin():
    """Admin panel page for managing UUDEX entities."""
    return rx.box(
        # Header
        rx.box(
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.icon("shield-check", size=32, color="white"),
                        rx.vstack(
                            rx.heading("UUDEX Administration", size="8", color="white", font_weight="bold"),
                            rx.text("Manage participants, subjects, and subscriptions",
                                   color="rgba(255,255,255,0.9)", font_size="lg"),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        # Admin entity selector - always visible
                        rx.hstack(
                            rx.vstack(
                                rx.text("Admin Entity:", color="rgba(255,255,255,0.8)", font_size="sm"),
                                rx.select(
                                    CertificateState.admin_display_names,
                                    placeholder="Select admin entity",
                                    on_change=AdminState.authenticate_admin,
                                    value=AdminState.selected_admin_entity,
                                    width="200px",
                                    size="2",
                                    bg="white",
                                ),
                                align_items="start",
                                spacing="1",
                            ),
                            rx.cond(
                                AdminState.is_authenticated,
                                rx.badge(
                                    rx.cond(
                                        AdminState.is_uudex_admin,
                                        "UUDEX Admin",
                                        rx.cond(
                                            AdminState.is_participant_admin,
                                            "Participant Admin",
                                            "No Admin Rights"
                                        )
                                    ),
                                    color_scheme=rx.cond(
                                        AdminState.is_uudex_admin,
                                        "red",
                                        rx.cond(
                                            AdminState.is_participant_admin,
                                            "blue",
                                            "gray"
                                        )
                                    ),
                                    size="2",
                                    variant="solid",
                                ),
                            ),
                            rx.link(
                                rx.button(
                                    rx.icon("home", size=18, margin_right="8px"),
                                    "Home",
                                    variant="outline",
                                    color_scheme="gray",
                                    size="2",
                                ),
                                href="/",
                            ),
                            spacing="3",
                            align_items="center",
                        ),
                        align_items="center",
                        width="100%",
                    ),
                    spacing="6",
                    padding_y="8",
                ),
                max_width="1200px",
            ),
            background="linear-gradient(135deg, #dc2626 0%, #991b1b 100%)",
            width="100%",
            box_shadow="0 4px 20px rgba(0,0,0,0.1)",
        ),

        # Main content
        rx.container(
            rx.vstack(
                # Status notification
                rx.cond(
                    AdminState.show_status,
                    rx.box(
                        rx.hstack(
                            rx.icon(
                                rx.cond(AdminState.status_is_error, "alert_circle", "check_circle_2"),
                                size=20,
                                color=rx.cond(AdminState.status_is_error, "red.500", "green.500"),
                            ),
                            rx.text(
                                AdminState.status_message,
                                font_weight="medium",
                                color=rx.cond(AdminState.status_is_error, "red.700", "green.700"),
                            ),
                            rx.spacer(),
                            rx.icon(
                                "x",
                                size=18,
                                cursor="pointer",
                                on_click=AdminState.close_status,
                                color="gray.400",
                                _hover={"color": "gray.600"},
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        padding="4",
                        bg=rx.cond(AdminState.status_is_error, "red.50", "green.50"),
                        border="1px solid",
                        border_color=rx.cond(AdminState.status_is_error, "red.200", "green.200"),
                        border_radius="lg",
                        margin_bottom="6",
                        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                    ),
                ),

                # Authentication message when no entity selected
                rx.cond(
                    ~AdminState.is_authenticated,
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("lock", size=20, color="red.500"),
                                rx.heading("Authentication Required", size="6", color="gray.700"),
                                align_items="center",
                                spacing="2",
                            ),
                            rx.divider(color="gray.200"),
                            rx.text(
                                "Please select an admin entity from the dropdown in the header to authenticate.",
                                font_weight="medium",
                                color="gray.600"
                            ),
                            align_items="start",
                            spacing="4",
                        ),
                        background="white",
                        border="1px solid",
                        border_color="red.200",
                        border_radius="xl",
                        padding="6",
                        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                        margin_bottom="6",
                    ),
                ),

                # Admin content (only shown when authenticated)
                rx.cond(
                    AdminState.is_authenticated,
                    rx.vstack(
                        # Navigation tabs - conditionally show based on permissions
                        rx.box(
                            rx.hstack(
                                # Participants tab - visible to all admins
                                rx.button(
                                    rx.hstack(
                                        rx.icon("users", size=16),
                                        rx.text("Participants"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    on_click=lambda: AdminState.set_section("participants"),
                                    color_scheme=rx.cond(AdminState.current_section == "participants", "blue", "gray"),
                                    variant=rx.cond(AdminState.current_section == "participants", "solid", "outline"),
                                    size="2",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon("server", size=16),
                                        rx.text("Endpoints"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    on_click=lambda: AdminState.set_section("endpoints"),
                                    color_scheme=rx.cond(AdminState.current_section == "endpoints", "blue", "gray"),
                                    variant=rx.cond(AdminState.current_section == "endpoints", "solid", "outline"),
                                    size="2",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon("database", size=16),
                                        rx.text("Subjects"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    on_click=lambda: AdminState.set_section("subjects"),
                                    color_scheme=rx.cond(AdminState.current_section == "subjects", "blue", "gray"),
                                    variant=rx.cond(AdminState.current_section == "subjects", "solid", "outline"),
                                    size="2",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon("bell", size=16),
                                        rx.text("Subscriptions"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    on_click=lambda: AdminState.set_section("subscriptions"),
                                    color_scheme=rx.cond(AdminState.current_section == "subscriptions", "blue", "gray"),
                                    variant=rx.cond(AdminState.current_section == "subscriptions", "solid", "outline"),
                                    size="2",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon("file-text", size=16),
                                        rx.text("Datasets"),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    on_click=lambda: AdminState.set_section("datasets"),
                                    color_scheme=rx.cond(AdminState.current_section == "datasets", "blue", "gray"),
                                    variant=rx.cond(AdminState.current_section == "datasets", "solid", "outline"),
                                    size="2",
                                ),
                                spacing="2",
                            ),
                            background="white",
                            padding="4",
                            border_radius="lg",
                            border="1px solid",
                            border_color="gray.200",
                            margin_bottom="6",
                        ),

                        # Content sections
                        rx.cond(
                            AdminState.current_section == "participants",
                            participants_section(),
                        ),
                        rx.cond(
                            AdminState.current_section == "endpoints",
                            endpoints_section(),
                        ),
                        rx.cond(
                            AdminState.current_section == "subjects",
                            subjects_section(),
                        ),
                        rx.cond(
                            AdminState.current_section == "subscriptions",
                            subscriptions_section(),
                        ),
                        rx.cond(
                            AdminState.current_section == "datasets",
                            datasets_section(),
                        ),

                        spacing="4",
                        width="100%",
                    ),
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


def participants_section():
    """Participants management section."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(
                        AdminState.is_participant_admin & ~AdminState.is_uudex_admin,
                        "My Participant",
                        "Participants"
                    ),
                    size="6",
                    color="gray.700"
                ),
                rx.spacer(),
                # Only show Add button for UUDEX admins
                rx.cond(
                    AdminState.is_uudex_admin,
                    rx.button(
                        rx.hstack(
                            rx.icon("plus", size=16),
                            rx.text("Add Participant"),
                            align_items="center",
                            spacing="2",
                        ),
                        on_click=AdminState.show_create_participant,
                        color_scheme="blue",
                        size="2",
                    ),
                ),
                align_items="center",
                width="100%",
            ),
            rx.divider(color="gray.200"),

            # Create participant form
            rx.cond(
                AdminState.show_create_participant_form,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Create New Participant", size="5", color="gray.700"),
                            rx.spacer(),
                            rx.button(
                                rx.icon("x", size=16),
                                on_click=AdminState.hide_create_participant,
                                variant="ghost",
                                color_scheme="gray",
                                size="1",
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        rx.grid(
                            rx.vstack(
                                rx.text("Short Name*", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.input(
                                    placeholder="Participant short name",
                                    value=AdminState.participant_form["participant_short_name"],
                                    on_change=lambda v: AdminState.update_participant_form("participant_short_name", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Long Name*", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.input(
                                    placeholder="Participant long name",
                                    value=AdminState.participant_form["participant_long_name"],
                                    on_change=lambda v: AdminState.update_participant_form("participant_long_name", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Description", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.text_area(
                                    placeholder="Optional description",
                                    value=AdminState.participant_form["description"],
                                    on_change=lambda v: AdminState.update_participant_form("description", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Root Org", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.select(
                                    ["Y", "N"],
                                    value=AdminState.participant_form["root_org_sw"],
                                    on_change=lambda v: AdminState.update_participant_form("root_org_sw", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            columns="2",
                            gap="4",
                        ),
                        rx.hstack(
                            rx.button(
                                "Cancel",
                                on_click=AdminState.hide_create_participant,
                                variant="outline",
                                color_scheme="gray",
                                size="2",
                            ),
                            rx.button(
                                rx.cond(
                                    AdminState.is_loading,
                                    rx.hstack(
                                        rx.spinner(size="1", color="white"),
                                        rx.text("Creating..."),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    rx.text("Create Participant"),
                                ),
                                on_click=AdminState.create_participant_submit,
                                color_scheme="blue",
                                size="2",
                                is_loading=AdminState.is_loading,
                            ),
                            justify="end",
                            spacing="2",
                            width="100%",
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    background="blue.50",
                    border="1px solid",
                    border_color="blue.200",
                    border_radius="lg",
                    padding="4",
                    margin_bottom="4",
                ),
            ),

            # Participants table
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Short Name", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Long Name", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Description", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Active", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Root Org", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Created", color="gray.600", font_weight="semibold"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AdminState.participants,
                            lambda participant: rx.table.row(
                                rx.table.cell(rx.text(participant["participant_short_name"], font_weight="medium")),
                                rx.table.cell(rx.text(participant["participant_long_name"])),
                                rx.table.cell(rx.text(participant.get("description", ""), color="gray.600")),
                                rx.table.cell(
                                    rx.badge(
                                        participant.get("active_sw", "Y"),
                                        color_scheme=rx.cond(participant.get("active_sw", "Y") == "Y", "green", "red"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        participant.get("root_org_sw", "N"),
                                        color_scheme=rx.cond(participant.get("root_org_sw", "N") == "Y", "blue", "gray"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        participant.get("create_datetime", ""),
                                        color="gray.500",
                                        font_size="sm",
                                    )
                                ),
                            ),
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
    )


def subjects_section():
    """Subjects management section."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Subjects", size="6", color="gray.700"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Add Subject"),
                        align_items="center",
                        spacing="2",
                    ),
                    on_click=AdminState.show_create_subject,
                    color_scheme="green",
                    size="2",
                ),
                align_items="center",
                width="100%",
            ),
            rx.divider(color="gray.200"),

            # Subjects table
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Dataset Key", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Type", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Queue Size", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Priority", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Owner", color="gray.600", font_weight="semibold"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AdminState.subjects,
                            lambda subject: rx.table.row(
                                rx.table.cell(rx.text(subject["subject_name"], font_weight="medium")),
                                rx.table.cell(rx.text(subject["dataset_instance_key"], font_family="mono")),
                                rx.table.cell(
                                    rx.badge(
                                        subject["subscription_type"],
                                        color_scheme="blue",
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(rx.text(f"{subject.get('max_queue_size_kb', 0)} KB")),
                                rx.table.cell(rx.text(str(subject.get("priority", 0)))),
                                rx.table.cell(rx.text(str(subject.get("owner_participant_id", "")))),
                            ),
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
    )


def subscriptions_section():
    """Subscriptions management section."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Subscriptions", size="6", color="gray.700"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Add Subscription"),
                        align_items="center",
                        spacing="2",
                    ),
                    on_click=AdminState.show_create_subscription,
                    color_scheme="purple",
                    size="2",
                ),
                align_items="center",
                width="100%",
            ),
            rx.divider(color="gray.200"),

            # Subscriptions table
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("State", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Owner Endpoint", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("UUID", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Created", color="gray.600", font_weight="semibold"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AdminState.subscriptions,
                            lambda subscription: rx.table.row(
                                rx.table.cell(rx.text(subscription["subscription_name"], font_weight="medium")),
                                rx.table.cell(
                                    rx.badge(
                                        subscription["subscription_state"],
                                        color_scheme=rx.cond(
                                            subscription["subscription_state"] == "ACTIVE",
                                            "green",
                                            "gray"
                                        ),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(rx.text(str(subscription.get("owner_endpoint_id", "")))),
                                rx.table.cell(
                                    rx.text(
                                        subscription.get("subscription_uuid", ""),
                                        font_family="mono",
                                        font_size="sm",
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        subscription.get("create_datetime", ""),
                                        color="gray.500",
                                        font_size="sm",
                                    )
                                ),
                            ),
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
    )


def endpoints_section():
    """Endpoints management section."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    rx.cond(
                        AdminState.is_participant_admin & ~AdminState.is_uudex_admin,
                        "My Participant's Endpoints",
                        "Endpoints"
                    ),
                    size="6",
                    color="gray.700"
                ),
                rx.spacer(),
                # Both UUDEX admins and participant admins can add endpoints
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Add Endpoint"),
                        align_items="center",
                        spacing="2",
                    ),
                    on_click=AdminState.show_create_endpoint,
                    color_scheme="purple",
                    size="2",
                ),
                align_items="center",
                width="100%",
            ),
            rx.divider(color="gray.200"),

            # Create endpoint form
            rx.cond(
                AdminState.show_create_endpoint_form,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Create New Endpoint", size="5", color="gray.700"),
                            rx.spacer(),
                            rx.button(
                                rx.icon("x", size=16),
                                on_click=AdminState.hide_create_endpoint,
                                variant="ghost",
                                color_scheme="gray",
                                size="1",
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        rx.grid(
                            rx.vstack(
                                rx.text("Username*", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.input(
                                    placeholder="Endpoint username",
                                    value=AdminState.endpoint_form["endpoint_user_name"],
                                    on_change=lambda v: AdminState.update_endpoint_form("endpoint_user_name", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Certificate DN*", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.input(
                                    placeholder="Distinguished Name",
                                    value=AdminState.endpoint_form["certificate_dn"],
                                    on_change=lambda v: AdminState.update_endpoint_form("certificate_dn", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Participant*", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.cond(
                                    AdminState.is_participant_admin & ~AdminState.is_uudex_admin,
                                    # Participant admins see a read-only field
                                    rx.input(
                                        value=AdminState.endpoint_form["participant_id"],
                                        is_disabled=True,
                                        width="100%",
                                    ),
                                    # UUDEX admins can enter participant ID
                                    rx.input(
                                        placeholder="Participant ID",
                                        value=AdminState.endpoint_form["participant_id"],
                                        on_change=lambda v: AdminState.update_endpoint_form("participant_id", v),
                                        width="100%",
                                        type="number",
                                    ),
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Active", font_weight="medium", color="gray.600", font_size="sm"),
                                rx.select(
                                    ["Y", "N"],
                                    value=AdminState.endpoint_form["active_sw"],
                                    on_change=lambda v: AdminState.update_endpoint_form("active_sw", v),
                                    width="100%",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            # Admin permission fields - only for UUDEX admins
                            rx.cond(
                                AdminState.is_uudex_admin,
                                rx.vstack(
                                    rx.text("UUDEX Admin", font_weight="medium", color="gray.600", font_size="sm"),
                                    rx.select(
                                        ["Y", "N"],
                                        value=AdminState.endpoint_form["uudex_administrator_sw"],
                                        on_change=lambda v: AdminState.update_endpoint_form("uudex_administrator_sw", v),
                                        width="100%",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                            ),
                            rx.cond(
                                AdminState.is_uudex_admin,
                                rx.vstack(
                                    rx.text("Participant Admin", font_weight="medium", color="gray.600", font_size="sm"),
                                    rx.select(
                                        ["Y", "N"],
                                        value=AdminState.endpoint_form["participant_administrator_sw"],
                                        on_change=lambda v: AdminState.update_endpoint_form("participant_administrator_sw", v),
                                        width="100%",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                            ),
                            columns="2",
                            gap="4",
                        ),
                        rx.hstack(
                            rx.button(
                                "Cancel",
                                on_click=AdminState.hide_create_endpoint,
                                variant="outline",
                                color_scheme="gray",
                                size="2",
                            ),
                            rx.button(
                                rx.cond(
                                    AdminState.is_loading,
                                    rx.hstack(
                                        rx.spinner(size="1", color="white"),
                                        rx.text("Creating..."),
                                        align_items="center",
                                        spacing="2",
                                    ),
                                    rx.text("Create Endpoint"),
                                ),
                                on_click=AdminState.create_endpoint_submit,
                                color_scheme="purple",
                                size="2",
                                is_loading=AdminState.is_loading,
                            ),
                            justify="end",
                            spacing="2",
                            width="100%",
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    background="purple.50",
                    border="1px solid",
                    border_color="purple.200",
                    border_radius="lg",
                    padding="4",
                    margin_bottom="4",
                ),
            ),

            # Endpoints table
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Username", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Certificate DN", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Participant", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Active", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("UUDEX Admin", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Participant Admin", color="gray.600", font_weight="semibold"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AdminState.endpoints,
                            lambda endpoint: rx.table.row(
                                rx.table.cell(rx.text(endpoint["endpoint_user_name"], font_weight="medium")),
                                rx.table.cell(rx.text(endpoint["certificate_dn"], font_family="mono", font_size="sm")),
                                rx.table.cell(rx.text(str(endpoint.get("participant_id", "")))),
                                rx.table.cell(
                                    rx.badge(
                                        endpoint.get("active_sw", "Y"),
                                        color_scheme=rx.cond(endpoint.get("active_sw", "Y") == "Y", "green", "red"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        endpoint.get("uudex_administrator_sw", "N"),
                                        color_scheme=rx.cond(endpoint.get("uudex_administrator_sw", "N") == "Y", "red", "gray"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        endpoint.get("participant_administrator_sw", "N"),
                                        color_scheme=rx.cond(endpoint.get("participant_administrator_sw", "N") == "Y", "blue", "gray"),
                                        variant="soft",
                                    )
                                ),
                            ),
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
    )


def datasets_section():
    """Datasets management section."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Datasets", size="6", color="gray.700"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Add Dataset"),
                        align_items="center",
                        spacing="2",
                    ),
                    on_click=AdminState.show_create_dataset,
                    color_scheme="orange",
                    size="2",
                ),
                align_items="center",
                width="100%",
            ),
            rx.divider(color="gray.200"),

            # Datasets table
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Description", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Size", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Subject ID", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Owner", color="gray.600", font_weight="semibold"),
                            rx.table.column_header_cell("Created", color="gray.600", font_weight="semibold"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            AdminState.datasets,
                            lambda dataset: rx.table.row(
                                rx.table.cell(rx.text(dataset["dataset_name"], font_weight="medium")),
                                rx.table.cell(rx.text(dataset.get("description", ""), color="gray.600")),
                                rx.table.cell(rx.text(f"{dataset.get('payload_size', 0)} bytes")),
                                rx.table.cell(rx.text(str(dataset.get("subject_id", "")))),
                                rx.table.cell(rx.text(str(dataset.get("owner_participant_id", "")))),
                                rx.table.cell(
                                    rx.text(
                                        dataset.get("create_datetime", ""),
                                        color="gray.500",
                                        font_size="sm",
                                    )
                                ),
                            ),
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
    )
