from flet import (AppBar, Column, Dropdown, ElevatedButton, FilePicker, FilePickerResultEvent,
                  FilePickerUploadEvent, FilePickerUploadFile, Page, ProgressRing, Ref, Row, Text,
                  View, colors, dropdown, icons, ControlEvent)

import logging
from uudex_web.settings import UUDEXSettings as settings
from pathlib import Path
from functools import partial
from uudex_web.views.common import build_certificates_dropdown, build_subject_dropdown

import uudex_api_client.models as md
from uudex_web.data.certificates import Certificate, set_session_certificate
from uudex_web.data import get_subjects
from typing import Callable

_log = logging.getLogger(__name__)

certificate_dropdown = Ref[Dropdown]()
subject_dropdown = Ref[Dropdown]()
upload_row = Ref[Row]()

this_view = Ref[View]()
this_page = Ref[Page]()
file_picker = Ref[FilePicker]()
selected_files = Ref[Text]()
send_button = Ref[ElevatedButton]()
send_results = Ref[Text]()


def sender_view(page: Page, get_certificates: Callable):
    page.title = "Sender Application"

    this_page.current = page

    controls = [
        AppBar(title=Text("Sender App"),
               bgcolor=colors.SURFACE_VARIANT,
               automatically_imply_leading=False),
        build_certificates_dropdown(get_certificates,
                                    on_change=on_change_certificate,
                                    ref=certificate_dropdown),
        FilePicker(on_result=pick_and_upload_results, ref=file_picker)
    ]

    this_view.current = View("/sender", controls=controls)
    return this_view.current


def pick_and_upload_results(e: FilePickerUploadEvent):

    uploads = []
    disable_send_button = True
    for f in file_picker.current.result.files:
        disable_send_button = False
        uploads.append(
            FilePickerUploadFile(f.name, upload_url=this_page.current.get_upload_url(f.name, 600)))
    send_button.current.disabled = disable_send_button
    file_picker.current.upload(uploads)
    selected_files.current.value = ", ".join(map(lambda f: f.name, e.files))
    this_view.current.update()


def send_files():
    for f in file_picker.current.result.files:
        pth = Path(f"{settings.upload_dir}").expanduser() / f.name
        if send_results.current.value is None:
            send_results.current.width = 500
            send_results.current.value = ""
        send_results.current.value = f"Loading: {f.name}\n" + send_results.current.value
        send_results.current.value = f"Sending: {f.name}\n" + send_results.current.value

    this_view.current.update()


def on_change_subject(e: ControlEvent):
    if upload_row.current is None:
        this_view.current.controls.append(
            Row([
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
        # allow_multiple = True if multiple files are necessary.
                    on_click=lambda _: file_picker.current.pick_files(dialog_title="Select Files"),
                ),
                ElevatedButton("Send",
                               icon=icons.SEND,
                               disabled=True,
                               on_click=lambda _: send_files(),
                               ref=send_button),
                ElevatedButton(
                    "Clear",
                    icon=icons.CLEAR,
        #disabled=True,
        #on_click=lambda _: send_files(),
        #ref=clear_button),
                ),
                Text(ref=selected_files)
            ]))
        this_view.current.controls.append(Row([Text(ref=send_results)]))

    this_view.current.update()


def on_change_certificate(e: ControlEvent):
    set_session_certificate(e.page.session_id, certificate=certificate_dropdown.current.value)
    if subject_dropdown.current is not None:
        build_subject_dropdown(partial(get_subjects, e.page.session_id),
                               on_change=on_change_subject,
                               ref=subject_dropdown)
        subject_dropdown.current.update()

    else:
        this_view.current.controls.append(
            build_subject_dropdown(partial(get_subjects, e.page.session_id),
                                   on_change=on_change_subject,
                                   ref=subject_dropdown))

    e.page.update()
