from datetime import datetime
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class LineItem(db.Model):
    """Model for Line Items."""

    __tablename__ = 'line_item'

    id = db.Column(db.String,
                   primary_key=True)
    parent_id = db.Column(db.String, db.ForeignKey('event.event_id'))

    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Line Item {}>'.format(self.quantity)

    def as_dict(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "quantity": self.quantity
        }

class Address(db.Model):
    """Model for Address."""

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String, db.ForeignKey('event.event_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    province = db.Column(db.String)
    country = db.Column(db.String)
    zip = db.Column(db.String)
    phone = db.Column(db.String)

    def __repr__(self):
        return '<Address {}>'.format(self.first_name)

    def as_dict(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "zip": self.zip,
            "phone": self.phone
        }

class Event(db.Model):
    """Model for Events."""

    __tablename__ = 'event'

    event_id = db.Column(db.String,
                         primary_key=True)
    event_type = db.Column(db.String)
    event_version = db.Column(db.String)
    ingestion_datetime_UTC = db.Column(db.DateTime, default=datetime.utcnow)
    lovevery_user_id = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    billing_address = db.relationship("Address", uselist=False)
    shipping_address = db.relationship("Address", uselist=False)
    currency = db.Column(db.String)
    financial_status = db.Column(db.String)
    order_value = db.Column(db.Float)
    total_discounts = db.Column(db.Float)
    total_tax = db.Column(db.Float)
    discount_codes = db.Column(db.String)
    buyer_accepts_marketing = db.Column(db.Boolean)
    line_items = db.relationship("LineItem")

    def __repr__(self):
        return '<Event {}>'.format(self.event_id)

    def as_dict(self):
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "ingestion_datetime_UTC": self.ingestion_datetime_UTC,
            "lovevery_user_id": self.lovevery_user_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "billing_address": self.billing_address.as_dict(),
            "shipping_address": self.shipping_address.as_dict(),
            "currency": self.currency,
            "financial_status": self.financial_status,
            "order_value": self.order_value,
            "total_discounts": self.total_discounts,
            "total_tax": self.total_tax,
            "buyer_accepts_marketing": self.buyer_accepts_marketing,
            "line_items": [line_item.as_dict() for line_item in self.line_items]
        }
