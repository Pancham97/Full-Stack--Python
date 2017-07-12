import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(
        String(80), nullable = False)
    id = Column(
        Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(
        String(80), nullable = False)
    id = Column(
        Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(
        Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    #Property of this class has to be indented correctly. For our case, it is named "serialize".
    @property
    def serialize(self):
        #Returns the object of JSON that can be read by humans easily.
        return {
            'Name': self.name,
            'Price': self.price,
            'ID': self.id,
            'Description': self.description,
            'Course': self.course,
        }

##End of file##
engine = create_engine(
    'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
