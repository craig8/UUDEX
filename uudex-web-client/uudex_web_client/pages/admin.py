import reflex as rx
from uudex_web_client.state import State


@rx.page(route="/admin")
def admin() -> rx.Component:
    """Admin interface for UUDEX configuration."""
    return rx.vstack(
        rx.heading("UUDEX Admin", size="3", mb=4),
        rx.button(
            "Back to Home",
            on_click=State.navigate("/"),
            size="1",
            position="absolute",
            top="4",
            left="4",
        ),
        align="center",
        justify="center",
        height="100vh",
        spacing="8",
    )
