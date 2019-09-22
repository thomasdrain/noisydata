import json
from sqlalchemy import create_engine
import os

def db_connect():
    # read config details
    with open('sql/config.json') as json_data_file:
        data = json.load(json_data_file)['mysql']

    # create engine to connect to RDS
    engine = create_engine("mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
                           .format(user = data['user'],
                                   pwd=data['passwd'],
                                   host = data['host'],
                                   port = data['port'],
                                   db = data['db']))

    return engine
