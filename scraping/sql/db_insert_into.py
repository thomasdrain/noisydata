

def db_insert_into(new_rows, table, engine):
    new_rows.to_sql(table, con = engine, if_exists = 'append', index = False)