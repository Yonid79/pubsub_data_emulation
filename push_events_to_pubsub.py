#!/usr/bin/python


import json
import os
import time
from fake_data_gen import player_session
from fake_retail_data import basket_orders
import threading
#from multiprocessing.pool import ThreadPool as Pool
import multiprocessing
import argparse
from google.cloud import pubsub_v1  #pip install google-cloud-pubsub

ap = argparse.ArgumentParser()
ap.add_argument("-ty", "--type", required=True,help="gaming or retail")
ap.add_argument("-e", "--env", required=True,help="local or gcp env")
ap.add_argument("-t", "--topic", required=True,help="topic")
ap.add_argument("-ep", "--project", required=True,help="project")
ap.add_argument("-th", "--threads", required=True,help="threads")

args = vars(ap.parse_args())

topic_name = args['topic']
project_id = args['project']
threads_count = int(args['threads'])
producer_type = args['type']


if args['env'] != 'gcp':
    os.environ['GOOGLE_CLOUD_DISABLE_GRPC'] = 'true'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~') + '/' + '.my_certificates/{}-b45eba100e04.json'.format(project_id)
    if os.environ.get('PUBSUB_EMULATOR_HOST'):
        del os.environ['PUBSUB_EMULATOR_HOST']


batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=512000,
    max_latency=1,  # One second
    max_messages=500
)

pubsub_client = pubsub_v1.PublisherClient(batch_settings)
topic_path = pubsub_client.topic_path(project_id, topic_name)


Total_rows_published =0

def send_session_to_pubsub(thread_id):
    print thread_id
    rows_count =0
    start = time.time()
    while True:
        sess = player_session()
        session_rows = sess.CreateSession()
        for r in sess.session_events:
            message_future = pubsub_client.publish(topic_path, data=r.encode('utf-8'))
            rows_count+=1

        if rows_count % 100 == 0:
            end = time.time()
            et = end - start
            rps = rows_count / et
            print('thread {} , published {} rows, rows/s = {}'.format(thread_id,rows_count,rps))


def send_basket_to_pubsub(thread_id):
    rows_count =0
    start = time.time()
    while True:
        bask = basket_orders()
        basket_rows = bask.basket_orders()
        for r in bask.basket:
            print r
            #message_future = pubsub_client.publish(topic_path, data=r.encode('utf-8'))
            rows_count+=1

        if rows_count % 100 == 0:
            end = time.time()
            et = end - start
            rps = rows_count / et
            print('thread {} , published {} rows, rows/s = {}'.format(thread_id,rows_count,rps))



def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=3):
        print('Publishing message on {} threw an Exception {}.'.format( topic_name, message_future.exception()))
    else:
        print(message_future.result())

#pool = Pool(threads_count)
threads = []


if producer_type=='retail':
    for i in range(0,threads_count):
        t = threading.Thread(target=send_basket_to_pubsub, args=(i, ))
        threads.append(t)
else:
    for i in range(0,threads_count):
        t = threading.Thread(target=send_session_to_pubsub, args=(i, ))
        threads.append(t)



for x in threads:
    x.start()
    time.sleep(1)

for x in threads:
    x.join()



while True:
    time.sleep(10)

print('Done')