import json
import logging
import os
import time
from kafka import KafkaConsumer

TOPIC_NAME = os.environ["KAFKA_TOPIC"]
logging.info('started listening ' + TOPIC_NAME)

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_URL = os.environ["KAFKA_URL"]

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_URL])


def save_in_db(location):
    from sqlalchemy import create_engine

    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    person_id = int(location["userId"])
    latitude, longitude = int(location["latitude"]), int(location["longitude"])

    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    logging.info(insert)
    conn.execute(insert)


while True:
    for item in consumer:
        message = item.value.decode('utf-8')
        logging.info('Processing message ', message)
        person_location_message = json.loads(message)
        save_in_db(person_location_message)
    logging.info("Waiting for new locations from person location events service")
    time.sleep(300)
