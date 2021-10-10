from app.udaconnect.models import Location, Person  # noqa
from app.udaconnect.schemas import LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as locations_api

    api.add_namespace(locations_api, path=f"/{root}")
