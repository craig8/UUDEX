import reflex as rx
from ..state import State


@rx.page(route="/")
def index() -> rx.Component:
    """Landing page with navigation buttons."""
    return rx.vstack(
        rx.heading("UUDEX Web Client", size="3", mb=4),
        rx.hstack(
            rx.button(
                "Sender",
                size="3",
                color_scheme="blue",
                on_click=State.navigate("/sender"),
            ),
            rx.button(
                "Receiver",
                size="3",
                color_scheme="green",
                on_click=State.navigate("/receiver"),
            ),
            rx.button(
                "Admin",
                size="3",
                color_scheme="purple",
                on_click=State.navigate("/admin"),
            ),
            spacing="4",
        ),
        align="center",
        justify="center",
        height="100vh",
        spacing="8",
    )
