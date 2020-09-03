import json

from flask import request, jsonify

from . import create_app, database
from .models import Event, Address, LineItem, db
import datetime
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    events = database.get_all(Event)
    events = [event.as_dict() for event in events]
    return jsonify(events), 200


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()

    new_event = _get_event(data)

    db.session.add(new_event)
    db.session.commit()
    return json.dumps("Added"), 200


def _get_event(event_data):
    event_dict = {}
    for key, value in event_data.items():
        if key == "billing_address" or key == "shipping_address":
            event_dict[key] = Address(**value)
        elif key == "line_items":
            event_dict[key] = [LineItem(**line_item) for line_item in value]
        else:
            event_dict[key] = value
    return Event(**event_dict)
