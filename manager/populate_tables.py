# this code comes after the table creation.
import os
import json
import random

from manager.model_list import MODELS
from manager.dbbasics import add, dict_to_dbinstance, add_from_dict
from manager.connection import connect, SCHEMA_NAME, connect_rc

from services.books_service import set_book_review
from services.purchases_service import add_to_cart, purchase_from_cart

from faker import Faker


def populate_tables():
    faker = Faker()

    # Create 10 users with their user profiles
    con = connect()        

    print ('# Filling <users>')
    for _ in range(10):
        email = faker.email()
        
        con.execute(f"insert into {SCHEMA_NAME}.user (email, password, role) values('{email}', '{faker.password()}', 'user')")
        con.execute(f"select userId from {SCHEMA_NAME}.user where email = '{email}'")
        
        userId = con.fetchone()[0]
        balance = faker.random_int(10, 1000)
        profilePicture = faker.file_path()
        country = faker.country().replace("'", "")
        nickName = faker.user_name()
        fullName = faker.name().replace("'", "")
        description = faker.text().replace("'", "")

        con.execute(f"Insert into {SCHEMA_NAME}.userprofile (Balance, ProfilePicture, Country, NickName, FullName, Description, UserId) values('{balance}', '{profilePicture}', '{country}', '{nickName}', '{fullName}', '{description}', '{userId}')")

    # Create 10 authors and books
    print ('# Filling <author>') 
    for i in range(10):
        first_name = faker.first_name().replace("'", "")
        last_name = faker.last_name().replace("'", "")
        con.execute(f"insert into {SCHEMA_NAME}.author (FirstName, LastName) values('{first_name}', '{last_name}')")

    # Create 5 publishers
    print ('# Filling <publishers>')
    for _ in range(5):
        country = faker.country().replace("'", "")
        name = faker.company().replace("'", "")
        con.execute(f"insert into {SCHEMA_NAME}.publisher (Country, Name) values('{country}', '{name}')")

    # Create 20 books
    print ('# Filling <books> <writenby>')
    for _ in range(20):
        title = faker.text(20).replace("'", "")
        coverImage = faker.file_path()
        publishDate = faker.date_time().strftime("%Y-%m-%d")
        price = faker.random_int(10, 1000)

        con.execute(f"select PublisherId from {SCHEMA_NAME}.publisher order by RANDOM() limit 1")
        publisherId = con.fetchone()[0]

        con.execute(f"insert into {SCHEMA_NAME}.book (Title, CoverImage, PublishDate, Price, PublisherId) values('{title}', '{coverImage}', '{publishDate}', '{price}', '{publisherId}') returning BookId")
        bookId = con.fetchone()[0]
        
        n_authors = faker.random_int() % 4 + 1 # up to 4 authors
        con.execute(f"\
                        insert into {SCHEMA_NAME}.writenby(AuthorId, BookId) \
                        select AuthorId, {bookId} as BookId from {SCHEMA_NAME}.author order by RANDOM() limit {n_authors}; \
                    ")
    con.execute('commit')

    # Create 100 items between purchases and reviews, simulating process for datamart populating
    print ('# Filling <purchases> and <reviews>')
    con = connect()
    con.execute(f"select UserId, BookId from {SCHEMA_NAME}.user join {SCHEMA_NAME}.book on 1=1 order by RANDOM() limit 200")
    pairs = con.fetchall()
    users_with_cart = set()
    bought_pair_unrated = set()
    rc = connect_rc()

    for i in range(200):
        print(i)
        random_number = random.randint(0, 5)
        # 0 -> add to cart
        # 1, 2 -> purchse cart
        # 3, 4, 5 -> add review
    
        if random_number in range(3, 6) and len(bought_pair_unrated) > 0: # add review
            userId, bookId = random.choice(list(bought_pair_unrated))
            bought_pair_unrated.remove((userId, bookId))
            rating = faker.random_int(1, 5)
            comment = faker.text(120).replace("'", "")
           
            query_data = {
                'UserId': userId,
                'BookId': bookId,
                'Rating': rating,
                'Comment': comment
            }
            set_book_review(query_data)
        
        elif random_number in range(1, 3) and len(users_with_cart) > 0:  # purchase cart from user
            userId = random.choice(list(users_with_cart))
            users_with_cart.remove(userId)
            
            cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"
            cart_items = rc.smembers(cart_key)
            for bookId in cart_items:
                bought_pair_unrated.add((userId, int(bookId))) 
            
            query_data = {
                'UserId': userId
            }
            purchase_from_cart(query_data)
        else:  # add to cart
            userId, bookId = pairs.pop()
            users_with_cart.add(userId)
            
            query_data = {
                'UserId': userId,
                'BookId': bookId,
            }
            add_to_cart(query_data)



def drop_tables():
    con = connect()

    con.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{SCHEMA_NAME.lower()}'")
    tables = con.fetchall()

    for table in tables:
        con.execute(f"DROP TABLE IF EXISTS {SCHEMA_NAME}.{table[0]} CASCADE")
    
    con.execute('commit')








