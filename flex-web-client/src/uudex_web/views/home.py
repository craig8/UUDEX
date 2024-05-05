from flet import AppBar, ElevatedButton, Page, Text, View, colors

from typing import Callable


import logging

_log = logging.getLogger(__name__)


def home_view(page: Page) -> View:
    return View("/", [
        AppBar(title=Text("Choose Application"),
               automatically_imply_leading=False,
               bgcolor=colors.SURFACE_VARIANT),
        ElevatedButton("Sender App", on_click=lambda _: page.go("/sender")),
        ElevatedButton("Subscriber App", on_click=lambda _: page.go("/subscriber")),
    ])
