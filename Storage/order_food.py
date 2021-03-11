from sqlalchemy import Column,  String, DateTime
from base import Base
import datetime


class order_food(Base):
    """ Order Food """

    __tablename__ = "order_food"

    order_id = Column(String, primary_key=True)
    drop_off_address = Column(String(250), nullable=False)
    drop_off_instructions = Column(String(250), nullable=False)
    restaurant_name = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self,order_id,drop_off_address, drop_off_instructions,restaurant_name):
        """ Initialize """

        self.drop_off_address = drop_off_address
        self.drop_off_instructions = drop_off_instructions
        self.order_id = order_id
        self.restaurant_name = restaurant_name
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of order food request"""
        dict = {}
        dict['drop_off_address'] = self.drop_off_address
        dict['drop_off_instructions'] = self.drop_off_instructions
        dict['order_id'] = self.order_id
        dict['restaurant_name'] = self.restaurant_name
        dict['date_created'] = self.date_created

        return dict
