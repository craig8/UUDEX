from flet import AppBar, ElevatedButton, Page, Text, View, colors, Dropdown, dropdown, ControlEvent
import uudex_api_client.models as md
from uudex_web.data.certificates import Certificate, set_session_certificate, get_certificate_by_name
from functools import partial
from uudex_web.views.common import build_certificates_dropdown
from typing import Callable
import logging
from uudex_web.data import get_subjects
import json

_log = logging.getLogger(__name__)

def subscriber_view(page: Page, get_certificates: Callable, get_message_list: Callable, get_message: Callable) -> View:
    certs: list[Certificate] = get_certificates() or []    # type: ignore

    set_session_certificate(page.session_id, certificate=certs[0])
    subjects = get_subjects(page.session_id)
    for v in subjects:
        print(v)

    return View("/subscriber", [
        build_certificates_dropdown(get_certificates, on_change=on_change_certificate),
    ])


def on_change_certificate(e: ControlEvent):

    cert = get_certificate_by_name(e.control.value)
    if not cert:
        raise KeyError("Invalid certificate specified in list.")

    _log.debug(e.page.session_id)

    set_session_certificate(e.page.session_id, cert)

    my_view: View = e.page.views[0]

    subjects = get_subjects(e.page.session_id)
    output = '\n'.join([str(s) for s in subjects])
    my_view.controls.append(Text(output))


    #e.page.views[0].controls.clear()
    #e.page.session.set("backend_cert", dd.options[dd.options.index])
    e.page.views[0].controls.append(Text("Wow is this how its done?"))
    e.page.update()
