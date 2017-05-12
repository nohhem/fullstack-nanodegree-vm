from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base,Shelter,Puppy
from database_setup import Base,Restaurant,MenuItem##
import datetime
from sqlalchemy import func

##engine = create_engine('sqlite:///puppyshelter.db')
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session= DBSession()

def q1():
    puppies = session.query(Puppy).order_by(Puppy.name)
    for p in puppies:
        print p.name


def q2():
    """Query all of the puppies that are less than 6 months old organized by the youngest first"""
    today = datetime.date.today()
    sixMonthsAgo = today - datetime.timedelta(days = 183)
    result = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

    # print the result with puppy name and dob
    for item in result:
        print "{name}: {dob}".format(name=item[0], dob=item[1])

def q3():
    result=session.query(Puppy).order_by(Puppy.weight.asc())
    for i in result:
        print i.weight

def q4():
    result1=session.query(Puppy).group_by(Puppy.shelter_id).all()
    """Query all puppies grouped by the shelter in which they are staying"""
    result = session.query(Shelter, func.count(Puppy.id)).group_by(Shelter.id)
    for item in result:
        print item[0].id, item[0].name, item[1]

def qrestaurants():
    l=[]
    restaurants=session.query(Restaurant)
    for r in restaurants:
        l.append(r.name)
    return l

qrestaurants()