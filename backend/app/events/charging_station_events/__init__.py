from flask import Blueprint

charging_stations = Blueprint("charging_stations", __name__)

from app.events.charging_station_events.init_ui_charging_stations_event import (
    init_ui_charging_stations_event,
)  # noqa

# Import all events to register routes
from app.events.charging_station_events.report_charging_station_event import (
    report_charging_station_event,
)  # noqa
from app.events.charging_station_events.search_postal_code_event import (
    search_postal_code_event,
)  # noqa
