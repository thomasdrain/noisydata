from sqlalchemy import types


def db_insert_into(new_rows, table, engine, operation='append'):

    # Update the datatypes to be inserted into DB, for all 'object' (AKA character) types in the table.
    # This ensures they don't get turned into CLOB type in Oracle, and use VARCHAR instead
    # (using max length of the text).

    new_data_types = {c: types.VARCHAR(new_rows[c].str.len().max())
                      for c in new_rows.columns[new_rows.dtypes == 'object'].tolist()}

    new_rows.to_sql(table, con=engine, if_exists=operation, index=False, chunksize=10000, dtype=new_data_types)
