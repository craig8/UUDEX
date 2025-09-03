import reflex as rx


class LandingState(rx.State):
    """State for the landing page."""

    pass


def landing():
    """Landing page with sender/receiver selection."""
    return rx.box(
        # Gradient background
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            z_index="-1",
        ),
        # Main content
        rx.center(
            rx.vstack(
                # Logo and title
                rx.vstack(
                    rx.icon(
                        "shield_check",
                        size=64,
                        color="white",
                    ),
                    rx.heading(
                        "UUDEX Sample App",
                        size="9",
                        color="white",
                        font_weight="bold",
                        text_align="center",
                    ),
                    spacing="4",
                    align_items="center",
                    margin_bottom="8",
                ),
                # Instruction text
                rx.text(
                    "Select your role to begin secure data transfer",
                    color="rgba(255,255,255,0.9)",
                    font_size="lg",
                    margin_bottom="6",
                ),
                # Selection cards
                rx.hstack(
                    # Sender card
                    rx.link(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon(
                                        "send",
                                        size=48,
                                        color="blue.500",
                                    ),
                                    padding="6",
                                    bg="blue.50",
                                    border_radius="full",
                                ),
                                rx.heading(
                                    "Send Data",
                                    size="6",
                                    color="gray.800",
                                    font_weight="bold",
                                ),
                                rx.text(
                                    "Upload and send data securely to registered entities",
                                    color="gray.600",
                                    text_align="center",
                                    font_size="md",
                                ),
                                rx.button(
                                    "Start as Sender",
                                    size="2",
                                    color_scheme="blue",
                                    width="100%",
                                    margin_top="4",
                                    border_radius="lg",
                                ),
                                spacing="4",
                                align_items="center",
                                padding="8",
                            ),
                            bg="white",
                            border_radius="xl",
                            box_shadow="0 10px 40px rgba(0,0,0,0.1)",
                            padding="2",
                            width="320px",
                            height="320px",
                            cursor="pointer",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 20px 60px rgba(0,0,0,0.15)",
                            },
                        ),
                        href="/sender",
                        target="_blank",
                        text_decoration="none",
                    ),
                    # Receiver card
                    rx.link(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon(
                                        "download",
                                        size=48,
                                        color="green.500",
                                    ),
                                    padding="6",
                                    bg="green.50",
                                    border_radius="full",
                                ),
                                rx.heading(
                                    "Receive Data",
                                    size="6",
                                    color="gray.800",
                                    font_weight="bold",
                                ),
                                rx.text(
                                    "Poll for and download data sent to your entity",
                                    color="gray.600",
                                    text_align="center",
                                    font_size="md",
                                ),
                                rx.button(
                                    "Start as Receiver",
                                    size="2",
                                    color_scheme="green",
                                    width="100%",
                                    margin_top="4",
                                    border_radius="lg",
                                ),
                                spacing="4",
                                align_items="center",
                                padding="8",
                            ),
                            bg="white",
                            border_radius="xl",
                            box_shadow="0 10px 40px rgba(0,0,0,0.1)",
                            padding="2",
                            width="320px",
                            height="320px",
                            cursor="pointer",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 20px 60px rgba(0,0,0,0.15)",
                            },
                        ),
                        href="/receiver",
                        target="_blank",
                        text_decoration="none",
                    ),
                    # Admin card
                    rx.link(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon(
                                        "shield_check",
                                        size=48,
                                        color="red.500",
                                    ),
                                    padding="6",
                                    bg="red.50",
                                    border_radius="full",
                                ),
                                rx.heading(
                                    "Administration",
                                    size="6",
                                    color="gray.800",
                                    font_weight="bold",
                                ),
                                rx.text(
                                    "Manage participants, subjects, and subscriptions",
                                    color="gray.600",
                                    text_align="center",
                                    font_size="md",
                                ),
                                rx.button(
                                    "Enter Admin Panel",
                                    size="2",
                                    color_scheme="red",
                                    width="100%",
                                    margin_top="4",
                                    border_radius="lg",
                                ),
                                spacing="4",
                                align_items="center",
                                padding="8",
                            ),
                            bg="white",
                            border_radius="xl",
                            box_shadow="0 10px 40px rgba(0,0,0,0.1)",
                            padding="2",
                            width="320px",
                            height="320px",
                            cursor="pointer",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-5px)",
                                "box_shadow": "0 20px 60px rgba(0,0,0,0.15)",
                            },
                        ),
                        href="/admin",
                        target="_blank",
                        text_decoration="none",
                    ),
                    spacing="8",
                    wrap="wrap",
                    justify="center",
                ),
                spacing="6",
                align_items="center",
            ),
            height="100vh",
            width="100%",
        ),
        height="100vh",
        width="100%",
        position="relative",
    )
