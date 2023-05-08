import argparse
import json

def make_args():
    global D_PARAM

    # create a parser object
    parser = argparse.ArgumentParser(description='Book Store App')

    # add arguments
    parser.add_argument('--setup', help='Create and populate all tables. Delete previous ones.', action='store_true')
    parser.add_argument('-q', help='Run a query given its name.', default=None)
    parser.add_argument('-d', help='Query data.', default="{}")

    # parse arguments
    args = parser.parse_args()
    args.d = json.loads(args.d)

    return args