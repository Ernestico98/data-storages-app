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
    for _ in range(10):
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

        con.execute(f"Insert into {SCHEMA_NAME}.userprofile (WalletKey, ProfilePicture, Country, NickName, FullName, Description, UserId) values('{walletKey}', '{profilePicture}', '{country}', '{nickName}', '{fullName}', '{description}', '{userId}')")

    # Create 10 authors and books 
    for i in range(10):
        con.execute(f"insert into {SCHEMA_NAME}.author (FirstName, LastName) values('{faker.first_name()}', '{faker.last_name()}')")

    # Create 5 publishers
    for _ in range(5):
        country = faker.country()
        name = faker.company()
        con.execute(f"insert into {SCHEMA_NAME}.publisher (Country, Name) values('{country}', '{name}')")

    # Create 20 books
    for _ in range(20):
        title = faker.text(20)
        coverImage = faker.file_path()
        publishDate = faker.date_time().strftime("%Y-%m-%d")
        price = faker.random_int(10, 1000)

        con.execute(f"select PublisherId from {SCHEMA_NAME}.publisher order by RANDOM() limit 1")
        publisherId = con.fetchone()[0]

        con.execute(f"select AuthorId from {SCHEMA_NAME}.author order by RANDOM() limit 1")
        authorId = con.fetchone()[0]

        con.execute(f"insert into {SCHEMA_NAME}.book (Title, CoverImage, PublishDate, Price, PublisherId, AuthorId) values('{title}', '{coverImage}', '{publishDate}', '{price}', '{publisherId}', '{authorId}')")


    # Create 100 purchases
    for _ in range(100):
        con.execute(f"select UserId from {SCHEMA_NAME}.user order by RANDOM() limit 1")
        userId = con.fetchone()[0]

        con.execute(f"select BookId from {SCHEMA_NAME}.book order by RANDOM() limit 1")
        bookId = con.fetchone()[0]

        purchaseDate = str(faker.date_time())

        con.execute(f"insert into {SCHEMA_NAME}.purchases (UserId, BookId, PurchaseDate) values('{userId}', '{bookId}', '{purchaseDate}')")

    for _ in range(50):
        con.execute(f"select UserId from {SCHEMA_NAME}.user order by RANDOM() limit 1")
        userId = con.fetchone()[0]

        con.execute(f"select BookId from {SCHEMA_NAME}.book order by RANDOM() limit 1")
        bookId = con.fetchone()[0]

        rating = faker.random_int(1, 5)
        comment = faker.text(120)

        con.execute(f"insert into {SCHEMA_NAME}.reviews (UserId, BookId, Rating, Comment) values('{userId}', '{bookId}', '{rating}', '{comment}')")

    con.execute('commit')


def drop_tables():
    con = connect()

    con.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{SCHEMA_NAME.lower()}'")
    tables = con.fetchall()

    for table in tables:
        con.execute(f"DROP TABLE IF EXISTS {SCHEMA_NAME}.{table[0]} CASCADE")
    
    con.execute('commit')








