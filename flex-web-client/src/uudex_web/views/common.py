from flet import Dropdown, dropdown
from uudex_web.data.certificates import Certificate
from typing import Callable

def build_certificates_dropdown(get_certificates: Callable, on_change: Callable) -> Dropdown:

    certs: list[Certificate] = get_certificates()
    drp_down = Dropdown(label="Select Certificate for API",
                        options=[dropdown.Option(text=cert.name, key=cert.name) for cert in sorted(certs, key=lambda cert: cert.name)],
                        on_change=on_change,
                        width=500)
    return drp_down


