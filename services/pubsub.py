from google.cloud import pubsub_v1
from fastapi import Depends
from typing import Annotated

def get_pubsub_client():
    publisher_client = pubsub_v1.PublisherClient()
    return publisher_client

PubSubPublisherClientDependency = Annotated[pubsub_v1.PublisherClient, Depends(get_pubsub_client)]

