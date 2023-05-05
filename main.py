#%%
import psycopg2, random, timeit
from timeit import default_timer as timer
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

#%%
def connect():
    database = os.getenv('DATABASE_NAME')
    user = os.getenv('DATABASE_USER')
    password = os.getenv('DATABASE_PASSWORD')
    host = os.getenv('DATABASE_HOST')
    port = os.getenv('DATABASE_PORT')
    
    conn = psycopg2.connect(database=database, user=user,
                            password=password, host=host, port=port)
    
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


