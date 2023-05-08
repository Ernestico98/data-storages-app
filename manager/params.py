import argparse


def make_args():
    # create a parser object
    parser = argparse.ArgumentParser(description='Book Store App')

    # add arguments
    parser.add_argument('--setup', help='Create and populate all tables. Delete previous ones.', action='store_true')

    # parse arguments
    args = parser.parse_args()

    return args