
def process_messages():

    try:
        """Process evnt process_messages"""
        hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
        client = KafkaClient(hosts=hostname)
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
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

    except:
        e = sys.exc_info()[0]
        log.info(str(e))



