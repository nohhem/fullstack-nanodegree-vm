import sys ##sys module provide number of funtions and variables
            ##that can be used to manipulate parts of python run-time environment

from sqlalchemy import Column,ForeignKey,Integer, String## will come in handy while writing our mapper code

from sqlalchemy.ext.declarative import declarative_base ## we will use it in configiration and class code


from sqlalchemy.orm import relationship #to creat our foreign key realtionships ##also will be used when writing our mapper
from sqlalchemy import create_engine ## we will use in our configuration code at the end of file

Base  = declarative_base()## this one (instatnce of declarative_base)will help us get set up when we begin to write our class code
                          ##The declativebase will let SQLALCHEY knows that our classes are special sqlalchemy classes
                          ## that correspon to tables in our database .
##################begining of our file ends here #######################################

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


####at the end of the file#######

engine = create_engine(
'sqlite:///restaurantmenu.db')## create instance of create_engine class and point to the database  we wil use
Base.metadata.create_all(engine) ## add the classes in our code as new tables in our database