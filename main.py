#%%
from dotenv import load_dotenv
load_dotenv()

from manager.connection import connect
from manager.setup_models import setup_models


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


# createTables()

setup_models()



