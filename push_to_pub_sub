#!/usr/bin/python


import json
import os
import time
from fake_data_gen import player_session
import threading
import argparse
from google.cloud import pubsub_v1  #pip install google-cloud-pubsub

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--env", required=True,help="local or gcp env")
ap.add_argument("-t", "--topic", required=True,help="topic")
ap.add_argument("-ep", "--project", required=True,help="project")

args = vars(ap.parse_args())

topic_name = args['topic']
project_id = args['project']

if args['env'] != 'gcp':
    os.environ['GOOGLE_CLOUD_DISABLE_GRPC'] = 'true'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~') + '/' + '.my_certificates/{}-b45eba100e04.json'.format(project_id)
    if os.environ.get('PUBSUB_EMULATOR_HOST'):
        del os.environ['PUBSUB_EMULATOR_HOST']


batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=2048,  # Two kilobyte
    max_latency=1,  # One second
)

pubsub_client = pubsub_v1.PublisherClient(batch_settings)
topic_path = pubsub_client.topic_path(project_id, topic_name)

def send_session_to_pubsub():
    while True:
        sess = player_session()
        session_rows = sess.CreateSession()
        print ('start {}').format(sess.user_id)
        for r in sess.session_events:
            #print(r)
            message_future = pubsub_client.publish(topic_path, data=r.encode('utf-8'))
            #message_future.add_done_callback(callback)

        print ('end {}').format(sess.user_id)



def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=3):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())


threads = []
for i in range(5):
    t = threading.Thread(target=send_session_to_pubsub)
    threads.append(t)
    t.start()

for x in threads:
    x.join()

# We must keep the main thread from exiting to allow it to process
# messages in the background.

while True:
    time.sleep(10)

print('Done')