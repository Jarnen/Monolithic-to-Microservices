import json
import os
import logging

from concurrent import futures
from kafka import KafkaProducer

import grpc

import person_location_event_pb2
import person_location_event_pb2_grpc

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

logging.info('Connecting to kafka ', KAFKA_URL)
print('Connecting to kafka ', KAFKA_URL)
logging.info('Connecting to kafka topic ', KAFKA_TOPIC)
print('Connecting to kafka topic ', KAFKA_TOPIC)

producer = KafkaProducer(bootstrap_servers=KAFKA_URL)


class PersonLocationEventServicer(person_location_event_pb2_grpc.ItemServiceServicer):

    def Create(self, request, context):
        request_value = {
            'userId': int(request.userId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }

        logging.info('processing entity ', request_value)

        person_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(KAFKA_TOPIC, person_encode_data)
        return person_location_event_pb2.PersonLocationEventMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_location_event_pb2_grpc.add_ItemServiceServicer_to_server(PersonLocationEventServicer(), server)

logging.info('Starting on port 5005')
server.add_insecure_port('[::]:5005')
server.start()
server.wait_for_termination()
