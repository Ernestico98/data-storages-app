# this code comes after the table creation.
import os
import json

from manager.model_list import MODELS

from manager.dbbasics import add, dict_to_dbinstance

def populate_tables():
    # First stage, load data from jsons
    for model in MODELS:
        json_name = os.path.join("data", model.__name__.lower() + ".json")
        
        if os.path.isfile(json_name):
            with open(json_name, "r") as file:
                content = file.read()
                content = json.loads(content)

                # list of objects
                if type(content) == list:
                    for pack in content:
                        add(dict_to_dbinstance(pack, model))
                # only one object
                else:
                    add(dict_to_dbinstance(content, model))

    # Second stage, generate some data randomly
