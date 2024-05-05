from flet import (AppBar, Column, Dropdown, ElevatedButton, FilePicker, FilePickerResultEvent,
                  FilePickerUploadEvent, FilePickerUploadFile, Page, ProgressRing, Ref, Row, Text,
                  View, colors, dropdown, icons, ControlEvent)

import logging
from uudex_web.settings import UUDEXSettings as settings
from pathlib import Path
from functools import partial
from uudex_web.views.common import build_certificates_dropdown

import uudex_api_client.models as md
from uudex_web.data.certificates import Certificate
from typing import Callable

_log = logging.getLogger(__name__)


def sender_view(page: Page, get_certificates: Callable, get_subjects: Callable):
    file_picker = FilePicker(on_result=pick_files_result, on_upload=on_file_picker_upload)

    selected_files = Text()
    files = Column()
    upload_button = ElevatedButton(
        "Upload",
        icon=icons.UPLOAD,
        on_click=upload_files,
        disabled=True,
    )



    # certs: list[Certificate] = get_certificates() or []    # type: ignore
    # cert_drop_down_options = [
    #     dropdown.Option(text=cert.name) for cert in certs
    # ]


    # subjects: list[md.Subject] = get_subjects() or []    # type: ignore
    # drop_down_options = [
    #     dropdown.Option(key=subject.subject_id, text=subject.subject_name)
    #     for subject in subjects
    # ]
    # drop_down_width = 400
    # dd_subjects = Dropdown(options=drop_down_options,
    #                         width=drop_down_width,
    #                         on_change=on_subject_change),
    controls = [
        build_certificates_dropdown(get_certificates, on_change=on_change_certificate),
        # Dropdown(label="Choose Certificate",
        #          options=cert_drop_down_options,
        #          on_change=partial(on_certificate_change, subject_drop_down=dd_subjects)),
        #dd_subjects,
    #    Row([
    #         ElevatedButton(
    #             "Pick files",
    #             icon=icons.UPLOAD_FILE,
    #             on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    #         ), selected_files
    #     ]),
    #     upload_button,
    # # ElevatedButton(
    # #     "Upload",
    # #     ref=upload_button,
    # #     icon=icons.UPLOAD,
    # #     on_click=upload_files,
    # #     disabled=True,
    # # ),
    #     ElevatedButton("Send", on_click=on_send_click),
    #     file_picker,
    #     selected_files,
    #     files,
    ]

    return View("/sender", controls=controls)

def upload_files(e):
    uf = []
    if file_picker.result is not None and file_picker.result.files is not None:
        for f in file_picker.result.files:
            pth = Path(f"{settings.upload_dir}").expanduser() / f.name
            _log.info(f"Uploading: {pth.as_posix()}")
            uf.append(
                FilePickerUploadFile(
                    f.name,
                    upload_url=pth.as_posix(),
                ))
        file_picker.upload(uf)

def on_file_picker_upload(e: FilePickerUploadEvent):
    print("File uploaded", e.data)

def pick_files_result(e: FilePickerUploadEvent):
    _log.debug(f"pick_files_result SELF IS: {id(self)}")
    upload_button.disabled = True if e.files is None else False
    progress_bars.clear()
    if len(files.controls) > 0:
        files.controls.clear()
    if e.files is not None:
        for f in e.files:
            prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            progress_bars[f.name] = prog
            files.controls.append(Row([prog, Text(f.name)]))

    # selected_files.value = (", ".join(map(lambda f: f.name, e.files))
    #                         if e.files else "Cancelled!")
    # selected_files.update()

def on_send_click(e):
    print("Send clicked")

def on_file_picker_result(e: FilePickerResultEvent):
    print("File picked", e.data)

def on_file_picker_upload(e: FilePickerUploadEvent):
    print("File uploaded", e.data)

def on_file_picker(e: FilePickerResultEvent):
    print("File picked", e.data)

def on_subject_change(e):
    print("Dropdown changed to", e.data)


def on_change_certificate(e: ControlEvent):
    _log.debug(f"Change for certficate {e}")
