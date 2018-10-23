import time
import os
import argparse
from google.cloud import pubsub_v1  #pip install google-cloud-pubsub

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--env", required=True,help="local or gcp env")
ap.add_argument("-t", "--sub", required=True,help="subscription_name")
ap.add_argument("-ep", "--project", required=True,help="project")

args = vars(ap.parse_args())

subscription_name = args['sub']
project_id = args['project']

if args['env'] != 'gcp':
    os.environ['GOOGLE_CLOUD_DISABLE_GRPC'] = 'true'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~') + '/' + '.my_certificates/{}-b45eba100e04.json'.format(project_id)
    if os.environ.get('PUBSUB_EMULATOR_HOST'):
        del os.environ['PUBSUB_EMULATOR_HOST']


subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(
    project_id, subscription_name)

def callback(message):
    print('Received message: {}'.format(message.data))
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)