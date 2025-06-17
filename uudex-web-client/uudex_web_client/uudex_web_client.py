import reflex as rx

from .certificate_state import CertificateState
from .sender import sender
from .receiver import receiver

# Configure and create the app
app = rx.App()
app.add_page(sender,
             route="/",
             on_load=CertificateState.load_entities_from_certs)
app.add_page(receiver,
             route="/receiver",
             on_load=CertificateState.load_entities_from_certs)
