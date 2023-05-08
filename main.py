from dotenv import load_dotenv
load_dotenv()

from manager.params import make_args
from manager.setup_models import setup_models
from manager.populate_tables import populate_tables, drop_tables

if __name__ == "__main__":
    args = make_args()

    if args.setup:
        # drop old tables
        drop_tables()

        # create tables
        setup_models()

        # fill all tables with some dummy data
        populate_tables()
