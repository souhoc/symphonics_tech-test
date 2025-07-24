from google.cloud import pubsub_v1
import logging


class PubSubRepository:
    """Repository for publishing and subscribing to Pub/Sub messages.

    This class encapsulates interactions with Google Cloud Pub/Sub,
    allowing for easy message publishing and subscription management.
    """

    def __init__(self, project_id: str):
        """Initializes the PubSubRepository with the given project ID.

        Args:
            project_id (Optional[str]): The Google Cloud project ID to use.
                                       If not provided, the environment variable
                                       'GOOGLE_CLOUD_PROJECT' is used.

        Attributes:
            project_id (str): The Google Cloud project ID.
            publisher_client (pubsub_v1.PublisherClient): Client for publishing messages.
            subscriber_client (pubsub_v1.SubscriberClient): Client for subscribing to messages.
            logger: Logger for logging information and errors.
        """

        self.logger = logging.getLogger("BigQueryRepository")
        self.project_id = project_id
        self.pub_client = pubsub_v1.PublisherClient()

        self.logger.info(
            "Initialized Pub/Sub Repository with project: %s", self.project_id
        )

    def publish_message(self, topic_name: str, message_data: str) -> str:
        """Publishes a message to the specified Pub/Sub topic.

        Args:
            topic_name (str): The name of the Pub/Sub topic to publish to.
            message_data (str): The message payload to send.

        Returns:
            str: The message ID of the published message.

        Raises:
            Exception: If there is an error during the publishing process.
        """
        topic_path = self.pub_client.topic_path(self.project_id, topic_name)

        try:
            future = self.pub_client.publish(
                topic_path, data=message_data.encode("utf-8")
            )
            message_id = future.result()
            self.logger.info(f"Published message with ID: {message_id}")
            return message_id
        except Exception as e:
            self.logger.error(
                f"Failed to publish message to topic {topic_name}: {str(e)}"
            )
            raise Exception(f"Failed to publish message: {str(e)}")
