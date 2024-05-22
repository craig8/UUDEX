from flet import AppBar, ElevatedButton, Page, Text, View, colors, Dropdown, dropdown, ControlEvent, Ref, Row, icons, DataTable, DataColumn, DataRow
import uudex_api_client.models as md
from uudex_web.data.certificates import Certificate, set_session_certificate, get_certificate_by_name
from functools import partial
from uudex_web.views.common import build_certificates_dropdown, build_subscription_dropdown
from typing import Callable
import logging
from uudex_web.data import get_subscriptions
import json

_log = logging.getLogger(__name__)

certificate_dropdown = Ref[Dropdown]()
subscription_dropdown = Ref[Dropdown]()

this_view = Ref[View]()
this_page = Ref[Page]()

action_row = Ref[Row]()
results_row = Ref[Row]()
results_datatable = Ref[DataTable]()


def subscriber_view(page: Page, get_certificates: Callable) -> View:
    page.title = "Subscriber Application"

    this_page.current = page

    controls = [
        AppBar(title=Text("Sender App"),
               bgcolor=colors.SURFACE_VARIANT,
               automatically_imply_leading=False),
        build_certificates_dropdown(get_certificates,
                                    on_change=on_change_certificate,
                                    ref=certificate_dropdown)
    ]

    this_view.current = View("/subscriber", controls=controls)
    return this_view.current


def on_subscription_change(e: ControlEvent):
    if action_row.current is None:
        this_view.current.controls.append(
            Row([
                ElevatedButton("List",
                               icon=icons.LIST
        # allow_multiple = True if multiple files are necessary.
        #on_click=lambda _: file_picker.current.pick_files(dialog_title="Select Files"),
                               ),
                ElevatedButton(text="Subscribe Dynamic", icon=icons.SUBSCRIPTIONS)
            ]))

    if results_row.current is None:
        results_row.current = Row([
            DataTable(ref=results_datatable,
                      columns=[DataColumn(label=Text("foo")),
                               DataColumn(label=Text("bar"))])
        ])
        this_view.current.controls.append(results_row.current)
    this_view.current.update()


def on_change_certificate(e: ControlEvent):
    set_session_certificate(e.page.session_id, certificate=certificate_dropdown.current.value)

    if subscription_dropdown.current is not None:
        build_subscription_dropdown(partial(get_subscriptions, e.page.session_id),
                                    on_change=on_subscription_change,
                                    ref=subscription_dropdown)
        subscription_dropdown.current.update()

    else:
        this_view.current.controls.append(
            build_subscription_dropdown(partial(get_subscriptions, e.page.session_id),
                                        on_change=on_subscription_change,
                                        ref=subscription_dropdown))

    e.page.update()
