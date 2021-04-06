from sqlalchemy import Column, String, DateTime
from base import Base
import datetime


class book_ride(Base):
    """ Ride request"""

    __tablename__ = "book_ride"

    ride_id = Column(String, primary_key=True)
    pickup_location = Column(String(250), nullable=False)
    destination_address = Column(String(250), nullable=False)
    pickup_notes = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, ride_id,pickup_location, destination_address, pickup_notes, ):
        """ Initialize """
        self.destination_address= destination_address
        self.pickup_location = pickup_location
        self.pickup_notes= pickup_notes
        self.ride_id = ride_id
        self.date_created = datetime.datetime.now()  # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of ride request"""
        dict = {}

        dict['ride_id'] = self.ride_id
        dict['pickup_location'] = self.pickup_location
        dict['destination_address'] = self.destination_address
        dict['pickup_notes'] = self.pickup_notes
        dict['date_created'] = self.date_created

        return dict
