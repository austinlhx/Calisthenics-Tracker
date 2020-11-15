from google.cloud import pubsub_v1
from google.cloud import storage
from concurrent.futures import TimeoutError

# TODO(developer)
project_id = "calistrack"
topic_id = "CalisTrackML"

def publish(project_id, topic_id, filename): 
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data = filename
    data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

    #print(f"Published messages to {topic_path}.")
def subscribe(project_id): 

    # TODO(developer)
    # project_id = "your-project-id"
    subscription_id = "CalisTrackML"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received {message}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=1000)
        except TimeoutError:
            streaming_pull_future.cancel()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))

def notification(bucket_name, name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    notification = bucket.get_notification(notification_id=name)
    return notification

bucket = "calistrack"
file = "pushups.mp4"
name = "pushup"
#notification(bucket)
subscribe(project_id)
upload_blob(bucket, file, name)
publish(project_id, topic_id, name)
#notification(bucket, name)


delete_blob(bucket, name)
