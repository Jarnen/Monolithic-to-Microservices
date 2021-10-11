import grpc

import person_location_event_pb2_grpc
import person_location_event_pb2

"""
Simulates user mobiles gps sending coordinates to grpc
"""

print("Sending coordinates...")

channel = grpc.insecure_channel("127.0.0.1:30007")
stub = person_location_event_pb2_grpc.ItemServiceStub(channel)

# Sample payload data
person_location_1 = person_location_event_pb2.PersonLocationEventMessage(
    userId=1,
    latitude=-500,
    longitude=60
)

# person_location_2 = person_location_event_pb2.PersonLocationEventMessage(
#     userId=5,
#     latitude=-100,
#     longitude=30
# )
#
# person_location_3 = person_location_event_pb2.PersonLocationEventMessage(
#     userId=6,
#     latitude=-200,
#     longitude=30
# )
#
# person_location_4 = person_location_event_pb2.PersonLocationEventMessage(
#     userId=8,
#     latitude=-200,
#     longitude=30
# )

response_1 = stub.Create(person_location_1)
# response_2 = stub.Create(person_location_2)
# response_3 = stub.Create(person_location_3)
# response_4 = stub.Create(person_location_4)

print("Coordinates sent...")
print(person_location_1, person_location_2, person_location_3, person_location_4)
