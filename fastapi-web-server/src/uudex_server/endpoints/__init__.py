from fastapi import FastAPI
from fastapi.routing import APIRoute
from .participant_endpoints import participant_router, participants_router
from .subject_endpoints import subject_router, subjects_router
from .uudex_endpoints import endpoint_router

tags_metadata = [{
    "name": "participants",
    "description": "Participants API"
}, {
    "name": "endpoints",
    "description": "Endpoints API"
}, {
    "name": "subjects",
    "description": "Subjects API"
}]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

def add_routers(app: FastAPI):
    if app.openapi_tags is None:
        app.openapi_tags = tags_metadata
    else:
        app.openapi_tags.extend(tags_metadata)
    app.include_router(participant_router, tags=["participants"])
    app.include_router(participants_router, tags=["participants"])
    app.include_router(endpoint_router, tags=["endpoints"])
    app.include_router(subject_router, tags=["subjects"])
    app.include_router(subjects_router, tags=["subjects"])

    # Simplify to the endpoint name rather than the whole trace of the
    # function using methods etc.
    use_route_names_as_operation_ids(app)
