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


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())



with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')


topics = app_config["events"]["topic"]

def get_OrderFood(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)
    logger.info("Retrieving OrderFood at index %d" %index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info("Message: %s" % msg)
            payload = msg["payload"]
            event= payload.ElementAt(index)
            return event,200

    except:
        logger.error("no message found")

    logger.error("could not find OrderFood at index %d" %index)
    return  {"message": "Not Found"}, 404



def get_BookRide(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)
    logger.info("Retrieving BookRide at index %d" %index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info("Message: %s" % msg)
            payload = msg["payload"]
            event= payload.ElementAt(index)
            return event,200

    except:
        logger.error("no message found")

    logger.error("could not find BookRide at index %d" %index)
    return  {"message": "Not Found"}, 404

app= connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)



if __name__== "__main__":
    app.run(port=8110)


