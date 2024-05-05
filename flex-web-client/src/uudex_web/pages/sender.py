import logging

import uudex_api_client.models as md
from flet import (AppBar, Column, Dropdown, ElevatedButton, FilePicker,
                  FilePickerResultEvent, FilePickerUploadEvent,
                  FilePickerUploadFile, Page, ProgressRing, Ref, Row, Text,
                  View, colors, dropdown, icons)

import uudex_web.data as data

_log = logging.getLogger(__name__)


def get_view(page: Page):
    return SenderView(subjects=data.get_subjects(), page=page)

class SenderView(View):
    def __init__(self, subjects: list[md.Subject], page: Page):
        self.page = page
        self.file_picker = FilePicker(on_result=self.pick_files_result, on_upload=self.on_file_picker_upload)
        self.selected_files = Text()
        self.files = Ref[Column]()
        self.upload_button = Ref[ElevatedButton]()
        self.progress_bars: dict[str, ProgressRing] = {}

        drop_down_options = [dropdown.Option(key=subject.subject_id, text=subject.subject_name) for subject in subjects]
        drop_down_width = 400
        controls = [
            AppBar(title=Text("Sender App"), bgcolor=colors.SURFACE_VARIANT, automatically_imply_leading=False),

            Dropdown(options=drop_down_options, width=drop_down_width,
                        on_change=self.on_subject_change),
            Row([
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: self.file_picker.pick_files(
                        allow_multiple=True
                    ),
                ),
                self.selected_files]
            ),
            ElevatedButton(
            "Upload",
            ref=self.upload_button,
            icon=icons.UPLOAD,
            on_click=self.upload_files,
            disabled=True,
        ),
            ElevatedButton("Send", on_click=self.on_send_click),
            self.file_picker,
            self.selected_files,
            Column(ref=self.files),
        ]
        super().__init__("/sender", controls)

    def upload_files(self, e):
        uf = []
        if self.file_picker.result is not None and self.file_picker.result.files is not None:
            for f in self.file_picker.result.files:
                _log.info(f"Uploading: {self.page.get_upload_url(f.name, 600)}")
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=self.page.get_upload_url(f.name, 600),
                    ))
            self.file_picker.upload(uf)

    def on_file_picker_upload(self, e: FilePickerUploadEvent):
        print("File uploaded", e.data)

    def pick_files_result(self, e: FilePickerUploadEvent):
        self.upload_button.current.disabled = True if e.files is None else False
        self.progress_bars.clear()
        if self.files.current is not None:
            self.files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                self.progress_bars[f.name] = prog
                self.files.current.controls.append(Row([prog, Text(f.name)]))
        self.update()
        # self.selected_files.value = (", ".join(map(lambda f: f.name, e.files))
        #                         if e.files else "Cancelled!")
        # self.selected_files.update()

    def on_send_click(self, e):
        print("Send clicked")

    def on_file_picker_result(self, e: FilePickerResultEvent):
        print("File picked", e.data)
    def on_file_picker_upload(self, e: FilePickerUploadEvent):
        print("File uploaded", e.data)

    def on_file_picker(self, e: FilePickerResultEvent):
        print("File picked", e.data)

    def on_subject_change(self, e):
        print("Dropdown changed to", e.data)
