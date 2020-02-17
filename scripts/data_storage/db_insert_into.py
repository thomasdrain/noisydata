

def db_insert_into(new_rows, table, engine, operation='append'):
    new_rows.to_sql(table, con=engine, if_exists=operation, index=False, chunksize=10000)