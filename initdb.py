import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

import pymysql
import pandas as pd
pymysql.install_as_MySQLdb()

Base = declarative_base()
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

# class Rider(db.Model):
#     __tablename__ = 'rider'
#     id = Column(db.Integer, primary_key=True)
#     bike_id = Column(db.Integer, nullable=False)
#     start_time = Column(db.Integer, nullable=False)
#     start_station_id = Column(db.Integer)
#     end_time = Column(db.Integer, nullable=False)
#     end_station_id = Column(db.Integer)
#     duration = Column(db.Integer, nullable=False)
#     user_type = Column(db.Integer, nullable=True)
#     member_age = Column(db.Integer, nullable=True)
#     member_gender = Column(db.Integer, nullable=True)

# class Station(db.Model):
#     __tablename__ = 'station'
#     id = Column(db.Integer, primary_key=True)
#     station_id = Column(db.Integer, unique=True, nullable=False)
#     station_name = Column(db.String(255), unique=True, nullable=False)
#     latitude = Column(db.Float, nullable=False)
#     longitude = Column(db.Float, nullable=False)
#     neighborhood = Column(db.String(255))
#     zipcode = Column(db.Integer)


class Rider(Base):
    __tablename__ = 'rider'
    id = Column(Integer, primary_key=True)
    bike_id = Column(Integer)
    start_time = Column(Integer)
    start_station_id = Column(Integer)
    end_time = Column(Integer)
    end_station_id = Column(Integer)
    duration = Column(Integer)
    user_type = Column(Integer)
    member_age = Column(Integer)
    member_gender = Column(Integer)
    
class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer)
    station_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    neighborhood = Column(String(255))
    zipcode = Column(Integer)


####  create SQL lite database - if it does not exist ####
engine = create_engine('sqlite:///GoBike.sqlite')
conn = engine.connect()

Base.metadata.create_all(engine)

#### ORM - object relational mechanism ####
from sqlalchemy.orm import Session
session = Session(bind=engine)

#### read CSV files and propagate SQL database ####

cleanfile = 'Data/stationsample_cleaned.csv'
df = pd.read_csv(cleanfile)

for index, row in df.iterrows():
    session.add(Station(station_id=row['station_id'],
                        station_name=row['station_name'], 
                        latitude=row['latitude'], 
                        longitude=row['longitude'], 
                        neighborhood=row['neighborhood'], 
                        zipcode=row['zipcode']))

file2 = 'Data/GoBikeRiderClean.csv'
df2 = pd.read_csv(file2)

# save point
session.begin_nested()

for index, row in df2.iterrows():
    session.add(Rider(bike_id = row['bike_id'],
                    start_time = row['start_time'],
                    start_station_id = row['start_station_id'],
                    end_time = row['end_time'],
                    end_station_id = row['end_station_id'],
                    duration = row['duration_sec'],
                    user_type = row['user_type'],
                    member_age = row['member_age'],
                    member_gender = row['member_gender']))

# commit staiton and rider data entries
session.commit()

# close session
session.close()


