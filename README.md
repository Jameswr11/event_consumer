# event_consumer

## Prerequisites:
1. Docker installed.
2. Docker Compose Installed

## How To Run
1. Clone this repository.
2. Run `docker-compose -f docker-compose.yml up -d`

## What It Does
This system is a Flask-SQLAlchemy application deployed in a Docker container that facilitates:
1. Storing new events in a PostgreSQL database.
2. Running a few canned analytical queries using the SQLAlchemy ORM library.

## Why this technology?
SQLAlchemy is the industry standard for interacting with a PostgreSQL database in Python. Pairing it with Flask for interaction only made sense. The system is designed to consume events as soon as they are made available. Since this is deployed to docker, it can be scaled horizontally using a container runner like Kubernetes to handle load. By wrapping the system in a web app, we are not limited to just consuming events in batch from files and can scale the system to handle any load of ingestion and analytical queries.

## Assumptions
1. The sample data given is actually not valid JSON (The nested fields are strings with multiple sets of nested double quotes). I edited the sample data to be valid json with the assumption that I would rather alter the producer to send valid json, rather than push those transformations onto every consumer.
2. I made an assumption that `order_value` would be available on each event, since it was not made available. 
3. I assumed that the timestamp of an event being sent to the consumer would be the timestamp used for analytical queries, since one was not made available.

## Test Data.
There is test data at the location `src/test/data/test_data.json`. I used this data when testing my API. Feel free to use it if you'd like to try out making requests to the system. 

## Example requests to the system using CURL.
### Get All
`curl --location --request GET 'http://localhost:5000/'`
### Create
```
curl --location --request POST 'http://0.0.0.0:5000/create' \
--header 'Content-Type: application/json' \
--data-raw '{
"event_type": "order.created",
"event_id": "dfacfc2362-6359-49d9-a445-27314e2ff7e6",
"event_version": "1.0.0",
"lovevery_user_id": "66f6",
"email": "dan.lovevery@gmail.com",
"first_name": "dan",
"last_name": "dyer",
"billing_address": {"first_name":"dan","last_name":"dyer","address1":"123 Main St","address2":"","city":"Boise","province":"Maryland","country":"United States","zip":"83702","phone":"208-860-6879"},
"shipping_address": {"first_name":"dan","last_name":"dyer","address1":"123 Main St","address2":"","city":"Boise","province":"Maryland","country":"United States","zip":"83702","phone":"208-860-6879"},
"currency": "USD",
"financial_status": "paid",
"order_value": 5.0,
"total_discounts": 0,
"total_tax": 0,
"discount_codes": "xxx",
"buyer_accepts_marketing": true,
"line_items": [{"quantity":"2","id":"2f31244085395571"}]
}'
```
### top 5 Customers
`curl --location --request GET 'http://localhost:5000/customers/top?start_date=2020-09-01&end_date=2020-09-05&count=5'`
### Order Value by day
`curl --location --request GET 'http://localhost:5000/orders/value?start_date=2020-09-01&end_date=2020-09-05&mode=DAY'`
### Total Order Value
`curl --location --request GET 'http://localhost:5000/orders/value?start_date=2020-09-01&end_date=2020-09-05&mode=TOTAL'`
### Sales By State
`http://localhost:5000/sales/province?start_date=2020-09-01&end_date=2020-09-05&province=Idaho`

## Testing
### Overview
I've implemented a framework for testing the application using Flask-Testing with setup and tear down scripts. All that is left to be done is actually write the unit tests. I've left this off due to time constraints.
### Test Plan
1. Write Unit Tests for each view with positive cases and negative cases. The negative cases can include: requests with malformed bodies, duplicate primary keys, empty data, Sending invalid, or unsupported query parameters.
2. Write Unit tests for each "public" function in the database section.

## Deployment
If I were to deploy this application in the cloud, I would deploy it to Kubernetes. Fortunately it is already a Docker Container, but it would require significant configuration updates. The database is unsecured and the default configuration. The webservice is not set up to take advantage of load balancing or auto scaling. All of this would need to be set up and configured based on the businesses needs.

## Final Thoughts
In a real system, I would write code to verify the integrity of the data being sent prior to attempting to load it into the database. Since I don't have the actual business rules, this seemed like an unnecessary exercise. I'd also implement real logging, error handling, and monitoring.
