import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

import pymysql
import pandas as pd
pymysql.install_as_MySQLdb()

Base = declarative_base()

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


