from dotenv import load_dotenv
load_dotenv()

from manager.setup_models import setup_models
from manager.populate_tables import populate_tables

if __name__ == "__main__":
    # create tables
    setup_models()

    # fill all tables with some dummy data
    populate_tables()
