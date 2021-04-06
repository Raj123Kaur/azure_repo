import connexion
import json
import os.path
from os import path
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import datetime
from pykafka import KafkaClient


#Functions

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())



with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')



topics = app_config['events']['topic']



def OrderFood(body):

    headers = {"Content-Type": "application/json"}
    logger.info("INFO: Received event OrderFood request with a unique id of %s" %body['order_id'] )
    hostname= "%s:%d"%(app_config['events']['hostname'],app_config['events']['port'])
    print(hostname)
    client = KafkaClient(hosts=hostname)
    print(client)
    topic = client.topics[str.encode(topics)]
    producer = topic.get_sync_producer()
    msg = {"type": "OrderFood",
           "datetime":
               datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body

           }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info("INFO: Returned event OrderFood response with a unique id of %s with status code 201" %(body['order_id']))
    return NoContent, 201



def BookRide(body):
    headers = {"Content-Type": "application/json"}
    logger.info("INFO: Received event BookRide request with a unique id of %s" %body['ride_id'])
    hostname = "%s:%d" % (app_config['events']['hostname'], app_config['events']['port'])
    print(hostname)
    client = KafkaClient(hosts=hostname)

    print(client)
    topic = client.topics[str.encode(topics)]
    producer = topic.get_sync_producer()

    msg = {"type": "BookRide",
           "datetime":
               datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body

           }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info("INFO: Returned event BookRide response with a unique id of %s with status code of 201" %(body['ride_id']))
    return NoContent, 201



app= connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__== "__main__":
    app.run(port=8080)
