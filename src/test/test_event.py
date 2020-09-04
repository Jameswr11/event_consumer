

import unittest
import random
import json
from flask import Flask
import flask_sqlalchemy

from flask_testing import TestCase
import os
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "password"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "event_db"
from src.models import db
from src import create_app

with open('./src/test/data/test_events.json', 'r') as f:
    test_data = json.load(f)


class EventTest(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
