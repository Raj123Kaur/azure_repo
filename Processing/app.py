import connexion
import json
import os.path
from os import path
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')
EVENT_FILE = app_config['datastore']['filename']


def populate_stats():
    logger.info("Start Periodic Processing")

    if os.path.exists(EVENT_FILE) == True:
        file = open(EVENT_FILE, "r")
        content = file.read()
        file.close()
        python_content = json.loads(content)
        url = app_config['eventstore']['url']
        # current_date_time= datetime.now()
        # current_date_time_n = current_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        current_date_time_n = python_content["current_date_time_n"]

        get = requests.get(url + "/requests/food-delivery?timestamp=" + current_date_time_n)
        logger.info("INFO: No of food delivery Received event %d" % len(get.json()))
        logger.error("ERROR: Did not receieve response code 200 %d" % get.status_code)

        get_t = requests.get(url + "/requests/ride-request?timestamp=" + current_date_time_n)
        logger.info("INFO:No of ride request Received event %d" % len(get_t.json()))
        logger.error("ERROR: Did not receieve response code 200 %d" % get_t.status_code)
        python_content["num_order_food_request"] += len(get.json())
        python_content["num_order_ride_request"] += len(get_t.json())
        current_date_time = datetime.now()
        python_content["current_date_time_n"] = current_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        json_content = json.dumps(python_content)

        f = open(EVENT_FILE, 'w')
        f.write(json_content)

        f.close()
        logger.debug("DEBUG: Updated statistics values %s,%s" % (get, get_t))
        logger.info(" Periodic Processing has ended")

    if os.path.exists(EVENT_FILE) == False:
        file = open(EVENT_FILE, "w")

        dict = {
            "num_order_food_request": 0,
            "num_order_ride_request": 0,
            "current_date_time_n": "2021-02-22T8:15:50"
        }
        dicts = json.dumps(dict)
        file.write(dicts)
        file.close()


def GetStats():
    logger.info("Request has started")
    if os.path.exists(EVENT_FILE) == True:
        file = open(EVENT_FILE, "r")
        content = file.read()
        python_content = json.loads(content)
        logger.debug("DEBUG: Updated statistics values %s" % python_content)
        logger.info("Request has completed")
        return python_content, 200
    if os.path.exists(EVENT_FILE) == False:
        logger.error("ERROR: Error")
        return 404, "statistics do not exist"


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)