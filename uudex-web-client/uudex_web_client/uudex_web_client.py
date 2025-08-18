import reflex as rx

from .certificate_state import CertificateState
from .sender import sender
from .receiver import receiver
from .landing import landing

# Configure and create the app
app = rx.App(
    stylesheets=[
        "/custom.css",  # Custom CSS for enhanced styling
    ],
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        scaling="100%",
    ),
)

app.add_page(
    landing,
    route="/",
    title="UUDEX Sample App",
    description="Choose between sending or receiving files",
)

app.add_page(
    sender,
    route="/sender",
    title="UUDEX - File Sender",
    description="Secure file transfer sender interface",
    on_load=CertificateState.load_entities_from_certs,
)

app.add_page(
    receiver,
    route="/receiver",
    title="UUDEX - File Receiver",
    description="Secure file transfer receiver interface",
    on_load=CertificateState.load_entities_from_certs,
)
