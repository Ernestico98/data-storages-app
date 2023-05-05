#%%
import psycopg2, random, timeit
from timeit import default_timer as timer
from datetime import timedelta

#%%
def connect():
    conn = psycopg2.connect(database="postgres", user="student", password="HSDStoTestDb3711", host="database-1.czcdhgn8biyx.us-east-1.rds.amazonaws.com", port="5432")
    return conn.cursor()


#%%
schemaName = 'BookSchema'

def createTables():
    con = connect()

    # Create schema
    con.execute(f"create schema if not exists {schemaName}")

    con.execute(f'create table {schemaName}.user( \
                                       \
                    )'
                );


    con.execute('commit')


def seedTables():
    pass


createTables()


