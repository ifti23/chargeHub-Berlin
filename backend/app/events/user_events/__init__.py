from flask import Blueprint

login_user = Blueprint("login_user", __name__)
register_user = Blueprint("register_user", __name__)

# Import all events to register routes
from app.events.user_events.user_login_event import user_login_event  # noqa
from app.events.user_events.user_registration_event import user_registration_event
