from .models import Event, Address, LineItem
from psycopg2.extras import DateRange
import logging
from flask import jsonify
import json
from . import db

def get_all_events():
    events = Event.query.all()

    return [event.as_dict() for event in events]


def add_event(data):
    event = _get_event(data)

    db.session.add(event)
    commit_changes()


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


def get_orders_value(start_date, end_date, mode):
    if mode == "TOTAL":
        return _get_orders_value_total(start_date, end_date)
    elif mode == "DAY":
        return _get_orders_value_by_day(start_date, end_date)
    else:
        raise ValueError('Invalid mode.')


def _get_orders_value_total(start_date, end_date):
    total_order_value = Event.query.filter(
        Event.ingestion_datetime_UTC.between(start_date, end_date)).with_entities(db.func.sum(Event.order_value)).first()[0]

    return total_order_value


def _get_orders_value_by_day(start_date, end_date):

    order_value_by_day = Event.query.filter(
        Event.ingestion_datetime_UTC.between(start_date, end_date)) \
        .with_entities(db.func.date(Event.ingestion_datetime_UTC),
                       db.func.sum(Event.order_value)) \
        .group_by(db.func.date(Event.ingestion_datetime_UTC)).all()

    response = []

    for row in order_value_by_day:
        response.append({
            "date": row[0],
            "order_value": row[1]
        })

    return response


def get_top_customers_with_marketing(start_date, end_date, count):
    customers = Event.query.filter(
        Event.ingestion_datetime_UTC.between(start_date, end_date)) \
        .filter(Event.buyer_accepts_marketing == True) \
        .with_entities(Event.lovevery_user_id) \
        .group_by(Event.lovevery_user_id) \
        .order_by(db.func.sum(Event.order_value).desc()) \
        .limit(count).first()

    return customers


def get_sales_by_province(start_date, end_date, province):
    sales = Event.query \
        .join(Address) \
        .join(LineItem) \
        .filter(Event.ingestion_datetime_UTC.between(start_date, end_date)) \
        .filter(Address.province == province) \
        .with_entities(LineItem.id, LineItem.quantity) \
        .group_by(Event.event_id, LineItem.id) \
        .all()
    logging.info(sales)

    response = []

    for row in sales:
        response.append({
            "id": row[0],
            "quantity": row[1],
        })
    return response


def commit_changes():
    db.session.commit()
