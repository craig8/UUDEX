import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import flet as ft
import flet.fastapi as flet_fastapi
from fastapi import FastAPI, Request
from flet import AppBar, Dropdown, ElevatedButton, Page, Text, View, colors, RouteChangeEvent


from .settings import UUDEXSettings as settings

logging.basicConfig(level=logging.getLevelName(settings.log_level))
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("flet_core").setLevel(logging.WARNING)
logging.getLogger("flet.fastapi").setLevel(logging.WARNING)

_log = logging.getLogger(__name__)

os.environ["FLET_SECRET_KEY"] = settings.secret_key


async def main(page: Page):
    import uudex_web.data as data
    from uudex_web.views import UUDEXViews as uudex_views

    try:
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.title = "UUDEX Sample Application"
        from .data import get_participants, get_subjects
        from .data.certificates import Certificate, get_certificates, set_session_certificate
        certs = get_certificates()
        set_session_certificate(page.session_id, certificate=certs[0])
        subjects = get_subjects(page.session_id)
        for v in subjects:
            print(v)
        # page.navigation_bar = ft.NavigationBar(destinations=[
        #     ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
        #     ft.NavigationDestination(
        #         icon=ft.icons.BOOKMARK_BORDER,
        #         selected_icon=ft.icons.BOOKMARK,
        #         label="Explore",
        #     ),
        # ])
        def route_change(e: RouteChangeEvent):
            page.views.clear()

            for p in uudex_views:
                if p.route == e.route:
                    page.views.append(p.instance(page=page))
                    break
            if not page.views:
                raise ValueError(f"The route {e.route} was not defined.")

            page.update()

        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    except Exception as e:
        _log.exception(e)

    # try:
    #     # Defautl route
    #     page.route = "/"

    #     # All the application routes are defined in the uudex_views object
    #     app_routes = [path(url=p.route, view=p.instance, clear=True) for p in uudex_views]

    #     # Routing the page to the appropriate route
    #     Routing(page=page, app_routes=app_routes)
    #     page.go(page.route)
    #     #page.go(page.route)
    # except Exception as e:
    #     _log.exception(e)



# Hook flet into FastAPI using flet.fastapi module
@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


# Create the fastapi app
app = FastAPI(lifespan=lifespan)

# Mount the flet app to the fastapi app.  More than one endpoint can be mounted to the same fastapi app.
app.mount(
    "/",
    flet_fastapi.app(main,
                     web_renderer=ft.WebRenderer.AUTO,
                     upload_dir=Path(settings.upload_dir).expanduser().as_posix()))
