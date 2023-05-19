from manager.connection import connect, SCHEMA_NAME, connect_rc
import datetime
from prettytable import PrettyTable
import json
from utils import datetime_deserializer, datetime_serializer

def get_purchases_count(guery_data):
    con = connect()
    con.execute(f"select count(*) from {SCHEMA_NAME}.purchases")
    
    ctn = con.fetchone()

    return ctn[0]


def get_purchases_by_user(query_data):
    UserId = query_data['UserId']

    con = connect()
    rc = connect_rc()

    cache_str = f"""{SCHEMA_NAME}_CACHE_get_purchases_by_user_{UserId}"""
    if rc.exists(cache_str):
        print('Is in cache')
        sol = json.loads(rc.get(cache_str), object_hook=datetime_deserializer)
    else:
        print('Is not in cache')
        con.execute(f"select * from {SCHEMA_NAME}.purchases where UserId={UserId}")
        sol = con.fetchall()
        rc.set(cache_str, json.dumps(sol, default=datetime_serializer))

    table = PrettyTable()
    table.field_names = ["UserId", "BookId", "PurchaseDate"]
    for row in sol:
        table.add_row(row)
    
    return table


def add_to_cart(query_data):

    try:
        con = connect()
        con.execute(f"""SELECT count(id)
                        FROM unnest(%s) AS id
                        WHERE id NOT IN (SELECT bookid FROM {SCHEMA_NAME}.book)""", ([query_data['BookId']],))
        
        ids = int(con.fetchone()[0])
        if ids > 0:
            return "The book provided doesn't exists in the store"

        rc = connect_rc()
        cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"
        rc.sadd(cart_key, query_data['BookId'])

        # fast stats 
        value_key = f"{SCHEMA_NAME}_stbookcart_{query_data['BookId']}"
        current_value = rc.get(value_key)
        current_value = 0 if current_value is None else int(current_value)
        current_value += 1
        rc.set(value_key, current_value)
        
    except Exception as e:
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"
    
    return "Book added successfully to the cart"

def remove_from_cart(query_data):

    try:
        rc = connect_rc()
        cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"
        rc.srem(cart_key, query_data['BookId'])

        # fast stats 
        value_key = f"{SCHEMA_NAME}_stbookcart_{query_data['BookId']}"
        current_value = rc.get(value_key)
        current_value = 0 if current_value is None else int(current_value)
        current_value = max(0, current_value-1)
        rc.set(value_key, current_value)

    except Exception as e:
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"
    
    return "Book removed successfully"

def purchase_from_cart(query_data):
    rc = connect_rc()
    cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"
    cart_items = rc.smembers(cart_key)
    cart_ids = [int(item) for item in cart_items]
    message = create_purchase({ 'UserId': query_data['UserId'], 'BooksIds': cart_ids })
    if message == "Purchase created successfully":
        clear_cart({'UserId': query_data['UserId']})
    return message

def get_cart_contents(query_data):
    rc = connect_rc()
    cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"
    cart_items = rc.smembers(cart_key)
    cart_ids = [int(item) for item in cart_items]
    return cart_ids

def clear_cart(query_data):

    try:
        rc = connect_rc()
        cart_key = f"{SCHEMA_NAME}_shop_cart_{query_data['UserId']}"

        # fast stats 
        cart_items = rc.smembers(cart_key)
        for item in cart_items:    
            value_key = f"{SCHEMA_NAME}_stbookcart_{int(item)}"
            rc.delete(value_key)

        rc.delete(cart_key)
    except Exception as e:
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"

    return "Cart cleared successfully"

def create_purchase(query_data):
    try:
         # invalidate cache for get_purchases_by_user
        rc = connect_rc()
        cache_str = f"""{SCHEMA_NAME}_CACHE_get_purchases_by_user_{query_data["UserId"]}"""
        rc.delete(cache_str)
        
        con = connect()
        con.execute("BEGIN")
        con.execute("set TRANSACTION ISOLATION LEVEL SERIALIZABLE;")

        books_ids_str = [str(i) for i in query_data['BooksIds']]
        books_ids = ','.join(books_ids_str)

        if len(books_ids_str) == 0:
            return "You must provide at least one book to buy"

        con.execute(f"""select count(*) from {SCHEMA_NAME}.purchases p
                    where p.userid = '{query_data['UserId']}' and p.bookid in ({books_ids})
                    """)
        
        amount_purchases = int(con.fetchone()[0])

        if amount_purchases > 0:
            return "User already puchased some of these books, please select books that the user doesn't own"

        con.execute(f"""select * from {SCHEMA_NAME}.user u
                        join {SCHEMA_NAME}.userprofile p on u.userid = p.userid
                        where u.userid = {query_data['UserId']}""")
        
        user_data = con.fetchone()
        if user_data == None:
            return "The UserId provided was not found, please provide a valid one"
        
        con.execute(f"""SELECT count(id)
                        FROM unnest(%s) AS id
                        WHERE id NOT IN (SELECT bookid FROM {SCHEMA_NAME}.book)""", (query_data['BooksIds'],))
        
        ids = int(con.fetchone()[0])
        if ids > 0:
            return "Some of the books ids provided were not found"

        con.execute(f"""select sum(b.price) from {SCHEMA_NAME}.book b 
                        where b.bookid  in ({books_ids})
                    """)

        total_price = con.fetchone()[0]
        user_balance = float(user_data[5].replace("$", "").replace(",", ""))
        books_price = float(total_price.replace("$", "").replace(",", ""))

        if user_balance < books_price:
            return "The user doesn't have enough balance to purchase the book"

        now = datetime.datetime.now()
        query = f"""insert into {SCHEMA_NAME}.purchases (UserId, BookId, PurchaseDate) 
                    values(%s, %s, %s)"""
        
        for i in books_ids_str:
            con.execute(query, (query_data['UserId'], i, now))
        
        con.execute(f"""update {SCHEMA_NAME}.userprofile
                        set balance = balance - {books_price}::money
                        where userid = {query_data['UserId']}
        """)

        con.execute("commit")

        # fast stats 
        for bid in query_data['BooksIds']:
            value_key = f"{SCHEMA_NAME}_stbookbuy_{int(bid)}"
            current_value = rc.get(value_key)
            current_value = 0 if current_value is None else int(current_value)
            current_value += 1
            rc.set(value_key, current_value)

        #  add purchase info to data mart
        for i in books_ids_str:
            create_data_mart_entry(query_data['UserId'], i, now)

    except Exception as e:
        con.execute("ROLLBACK")
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"
    return "Purchase created successfully"


def create_data_mart_entry(userId, bookId, date):
    try:
        con = connect()
        rc = connect_rc()
        con.execute(f"""select Price from {SCHEMA_NAME}.Book where BookId='{bookId}'""")

        price = float(con.fetchone()[0].replace("$", "").replace(",", ""))

        var_name = f"{SCHEMA_NAME}_reviewmean_{bookId}"
        value = rc.get(var_name)
        value = value.decode() if value is not None else "0:0"
        value = value.split(":")
        sum, cnt = int(value[0]), int(value[1])
        rating = 0 if cnt == 0 else sum / cnt

        # get amount of this book in some user's cart (This is stored in redis)
        value_key = f"{SCHEMA_NAME}_stbookcart_{bookId}"
        amount_in_cart = rc.get(value_key)
        amount_in_cart = (0 if amount_in_cart is None else int(amount_in_cart)) + 1

        # amount bought at buy time
        con.execute(f"""select count(*) from {SCHEMA_NAME}.purchases where BookId='{bookId}'""")
        amount_bought = con.fetchone()[0]
        
        con.execute(f"""insert into {SCHEMA_NAME}.datamart (UserId, BookId, DateTime, Price, Rating, Amount_In_Cart, Purchased_Amount) \
                        values('{userId}', '{bookId}', '{date}', '{price}', '{rating}', '{amount_in_cart}', '{amount_bought}')
                    """)
        con.execute('commit')
    except Exception as e:
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"
    
