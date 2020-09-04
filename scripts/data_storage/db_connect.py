import json
from sqlalchemy import create_engine
import os


def db_connect():
    dir_name = os.path.dirname(__file__)

    filename = os.path.join(dir_name, 'config.json')

    # read config details
    with open(filename) as json_data_file:
        data = json.load(json_data_file)['sql']

    connection_string = 'mssql+pyodbc://{username}:{password}@{hostname}:{port}/{database}?driver=SQL+Server+Native+Client+11.0'

    # create engine to connect to RDS
    print('Connecting to DB...')
    engine = create_engine(
        connection_string.format(
            username=data['user'],
            password=data['passwd'],
            hostname=data['host'],
            port=data['port'],
            database=data['db']
        )
    )
    print('Connected!\n')

    return engine
