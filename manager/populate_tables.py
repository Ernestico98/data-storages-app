# this code comes after the table creation.
import os
import json

from manager.model_list import MODELS
from manager.dbbasics import add, dict_to_dbinstance, add_from_dict
from manager.connection import connect, SCHEMA_NAME

from faker import Faker


# def populate_tables():
#     # First stage, load data from jsons
#     for model in MODELS:
#         json_name = os.path.join("data", model.__name__.lower() + ".json")
        
#         if os.path.isfile(json_name):
#             with open(json_name, "r") as file:
#                 content = file.read()
#                 content = json.loads(content)

#                 # list of objects
#                 if type(content) == list:
#                     for pack in content:
#                         add_from_dict(pack, model.__name__)
#                 # only one object
#                 else:
#                     add_from_dict(content, model.__name__)

#     # Second stage, generate some data randomly


def populate_tables():
    faker = Faker()

    # Create 10 users with their user profiles
    con = connect()        
    for i in range(10):
        email = faker.email()
        
        con.execute(f"insert into {SCHEMA_NAME}.user (email, password, role) values('{email}', '{faker.password()}', 'user')")
        con.execute(f"select userId from {SCHEMA_NAME}.user where email = '{email}'")
        
        userId = con.fetchone()[0]
        walletKey = faker.sha1()
        profilePicture = faker.file_path()
        country = faker.country()
        nickName = faker.user_name()
        fullName = faker.name()
        description = faker.text()

        con.execute(f"insert into {SCHEMA_NAME}.userprofile (WalletKey, ProfilePicture, Country, NickName, FullName, Description, UserId) values('{walletKey}', '{profilePicture}', '{country}', '{nickName}', '{fullName}', '{description}', '{userId}')")

    # Create 10 authors and books 
    for i in range(10):
        con.execute(f"insert into {SCHEMA_NAME}.author (FirstName, LastName) values('{faker.first_name()}', '{faker.last_name()}')")

    # Create 5 publishers
    

    con.execute('commit')








