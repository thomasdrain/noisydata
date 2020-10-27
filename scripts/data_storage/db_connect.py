import json
import pyodbc
from sqlalchemy import create_engine
import os


def db_connect():
    dir_name = os.path.dirname(__file__)

    filename = os.path.join(dir_name, 'config.json')

    # read config details
    with open(filename) as json_data_file:
        data = json.load(json_data_file)['sql']

    # Update me to move driver hardcoding to the config file
    connection_string = 'mssql+pyodbc://{username}:{password}@{hostname}:{port}/{database}?' \
                        'driver={driver}'

    driver = pyodbc.drivers()[0]

    # create engine to connect to RDS
    print('Connecting to DB...')
    engine = create_engine(
        connection_string.format(
            username=data['user'],
            password=data['passwd'],
            hostname=data['host'],
            port=data['port'],
            database=data['db'],
            driver=driver
        )
    )
    print('Connected!\n')

    return engine
