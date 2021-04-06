import connexion
import json
import os.path
from os import path
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from book_ride import book_ride
from order_food import order_food
import datetime
import yaml
import logging
import logging.config
import datetime

from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']
DB_ENGINE = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' %(user,password,hostname,port,db))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)



with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

logger.info('%s%d'%(hostname,port))


topics = app_config["events"]["topic"]
def get_OrderFood(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    orders = session.query(order_food).filter(order_food.date_created >= timestamp_datetime)
    results_list = []
    for order in orders:
        results_list.append(order.to_dict())
    session.close()
    logger.info("Query for Order Food  orders after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200




def get_BookRide(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    orders = session.query(book_ride).filter(book_ride.date_created >= timestamp_datetime)
    results_list = []
    for order in orders:
        results_list.append(order.to_dict())
    session.close()
    logger.info("Query for Book ride  orders after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def process_messages():


    """Process evnt process_messages"""
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False,
                                        auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "BookRide":  # Change this to your event type
            session = DB_SESSION()

            br = book_ride(payload['ride_id'],
                           payload['pickup_location'],
                           payload['destination_address'],
                           payload['pickup_notes'])

            session.add(br)

            session.commit()
            session.close()

            logger.debug("DEBUG: Stored event BookRide request with a unique id of %s" % payload['ride_id'])


        elif msg["type"] == "OrderFood": # Change this to your event type
            session = DB_SESSION()

            of = order_food(payload['order_id'],
                            payload['drop_off_address'],
                            payload['drop_off_instructions'],
                            payload['restaurant_name'])

            session.add(of)

            session.commit()
            session.close()
            logger.debug("DEBUG: Stored event OrderFood request with a unique id of %s" % payload['order_id'])



        consumer.commit_offsets()




app= connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__== "__main__":
    t1= Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
