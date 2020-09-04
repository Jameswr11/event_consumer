import json

from flask import request, jsonify

from . import create_app, database
from .models import Event, Address, LineItem, db
from datetime import datetime
import sys
import logging
from flask.json import JSONEncoder
from contextlib import suppress

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        # Optional: convert datetime objects to ISO format
        with suppress(AttributeError):
            return obj.isoformat()
        return dict(obj)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
app = create_app()
app.json_encoder = CustomJSONEncoder


@app.route('/', methods=['GET'])
def fetch():
    events = database.get_all_events()
    return jsonify(events), 200


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    database.add_event(data)

    return json.dumps("Added"), 200


@app.route('/orders/value', methods=['GET'])
def orders_value():
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    mode = request.args.get('mode')

    orders_value = database.get_orders_value(start_date, end_date, mode)

    return jsonify(orders_value), 200


@app.route('/customers/top', methods=['GET'])
def customers_top():
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    count = request.args.get('count')

    customers = database.get_top_customers_with_marketing(start_date, end_date, count)

    return jsonify(customers), 200


@app.route('/sales/province', methods=['GET'])
def sales_by_province():
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
    province = request.args.get('province')

    sales = database.get_sales_by_province(start_date, end_date, province)

    return jsonify(sales), 200
