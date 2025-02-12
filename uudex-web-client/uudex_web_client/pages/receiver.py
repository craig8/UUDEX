import reflex as rx
from uudex_web_client.state import State


@rx.page(route="/receiver")
def receiver() -> rx.Component:
    """Receiver interface for subscribing to data."""
    return rx.vstack(
        rx.heading("UUDEX Receiver", size="3", mb=4),
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
