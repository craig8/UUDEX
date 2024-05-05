import logging
from dataclasses import dataclass

import nicegui
from nicegui import ui, app
import benedict

from ..pages import Pages, show_global_header, get_uudex_label
from ..session import client_wrapper, time_request
from uudex_api_client.api.participants import get_all_participants_participants_get

_log = logging.getLogger(__name__)

page = Pages.HOME

state = benedict.benedict(parent_participant="")


@ui.page(page.value.uri, title=page.value.title)
def show_index(client: nicegui.Client, request: nicegui.storage.Request):
    import ssl
    from uudex_api_client.client import Client as APIClient
    from pprint import pprint
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(
        keyfile="certs/clients/4b3b819e-94bd-4adf-b461-17ccb58ac870__app_rt_1/client.key",
        certfile="certs/clients/4b3b819e-94bd-4adf-b461-17ccb58ac870__app_rt_1/client.pem")
    context.load_verify_locations(cafile="certs/clients/ca.crt")

    base_url = "https://localhost/api"
    # if not api_path.startswith("/"):
    #     api_path = f"/{api_path}"

    # if int(port) == 443:
    #     base_url = f"https://{host}{api_path}"
    # else:
    #     base_url = f"https://{host}:{port}{api_path}"
    api_client = APIClient(base_url=base_url, verify_ssl=context)
    print(request.headers)
    print(client)
    #with client_wrapper() as api_client:
    participants = get_all_participants_participants_get.sync(client=api_client)

    for p in participants:
        pprint(p.to_dict())
        #print(p)

    show_global_header(Pages.HOME.value)
    #    api_client = client_wrapper()
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    with ui.row():
        ui.label('your own page visits:')
        ui.label().bind_text_from(app.storage.user, 'count')

    print(app.storage.browser['id'])
    # if not app.storage.user.get('client'):
    #     app.storage.user['client'] = client
    # else:
    #     client = app.storage.user.get('client')

    print(client.id)
    #print(dir(app.storage))
    # print(f"_users {app.storage._users}")
    # print(dir(app.storage.browser))
    # print(dir(app.storage.general))
    #show_global_header(Pages.HOME)

    # wrapper = client_wrapper()

    # if wrapper is not None:
    #     print("Wrapper is not none")
    # else:
    #     print("Wrapper was none")

    # def on_select_parent_participant(new_participant: str):
    #     response_time = None
    #     if new_participant is None:
    #         return

    #     if new_participant != state.parent_participant:
    #         state.parent_participant = parent_participant.value
    #         response_time = time_request(new_participant,
    #                                      client_wrapper().get_parent_participant, new_participant)
    #         print(response_time.response)

    #     uuid_label = ui.label(f"Participant UUID: ")
    #     name_label = ui.label(f"Participant Name: ")
    #     description_label = ui.label(f"Description: ")
    #     duration_label = ui.label(f"Execution Time: ")

    # with ui.row():
    #     with ui.column():
    #         user_select_list = [x for x in client_wrapper()._all_users]
    #         parent_participant = ui.select(user_select_list, label="Parent Participant", with_input=True,
    #                                        on_change=lambda e: on_select_parent_participant(e.value)).classes("w-64")
