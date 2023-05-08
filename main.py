from dotenv import load_dotenv
load_dotenv()

from manager.params import make_args
from manager.setup_models import setup_models
from manager.populate_tables import populate_tables, drop_tables

from services.purchases_service import get_purchases_count, get_purchases_by_user

QUERIES = {
    "get_purchases_count":get_purchases_count,
    "get_purchases_by_user":get_purchases_by_user,
}

if __name__ == "__main__":
    args = make_args()

    if args.setup:
        # drop old tables
        drop_tables()

        # create tables
        setup_models()

        # fill all tables with some dummy data
        populate_tables()
    
    # run some query
    if args.q:
        fun = QUERIES[args.q]
        sol = fun(args.d)
        
        print ("QUERY:", args.q)
        print (sol)
