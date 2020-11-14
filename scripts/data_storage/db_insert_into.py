#from sqlalchemy import types
#import pandas as pd
import os


def db_insert_into(new_rows, table, engine, operation='append', local=''):

    # Update the datatypes to be inserted into DB, for all 'object' (AKA character) types in the table.
    # This ensures they don't get turned into CLOB type in Oracle, and use VARCHAR instead
    # (using max length of the text).

    #new_data_types = {c: types.VARCHAR(new_rows[c].str.len().max())
    #                  for c in new_rows.columns[new_rows.dtypes == 'object'].tolist()}

    if local != '':
        # If file exists, create it
        if not os.path.isfile(local):
            new_rows.to_csv(local, header='column_names')
        # Otherwise append without writing the header
        else:
            new_rows.to_csv(local, mode='a', header=False)

    if table != '':
        new_rows.to_sql(table, con=engine, if_exists=operation, index=False, chunksize=1000)#, dtype=new_data_types)
