import reflex as rx
from ..state import State


@rx.page(route="/sender")
def sender() -> rx.Component:
    """Sender interface for publishing data."""
    return rx.vstack(
        rx.heading("UUDEX Sender", size="3", mb=4),
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
