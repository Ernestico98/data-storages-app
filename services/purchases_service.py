from manager.connection import connect, SCHEMA_NAME
import datetime
from prettytable import PrettyTable

def get_purchases_count(guery_data):
    con = connect()
    con.execute(f"select count(*) from {SCHEMA_NAME}.purchases")
    
    ctn = con.fetchone()

    return ctn[0]


def get_purchases_by_user(query_data):
    UserId = query_data['UserId']

    con = connect()
    con.execute(f"select * from {SCHEMA_NAME}.purchases where UserId={UserId}")

    sol = con.fetchall()

    table = PrettyTable()
    table.field_names = ["UserId", "BookId", "PurchaseDate"]
    for row in sol:
        table.add_row(row)
    
    return table

def create_purchase(query_data):
    try:

        con = connect()
        con.execute("BEGIN")
        con.execute("set TRANSACTION ISOLATION LEVEL SERIALIZABLE;")

        con.execute(f"""select count(*) from {SCHEMA_NAME}.purchases p
                    where p.userid = '{query_data['UserId']}' and p.bookid = '{query_data['BookId']}'
                    """)
        
        amount_purchases = int(con.fetchone()[0])

        if amount_purchases > 0:
            return "User already puchased this book"

        con.execute(f"""select * from {SCHEMA_NAME}.user u
                        join {SCHEMA_NAME}.userprofile p on u.userid = p.userid
                        where u.userid = {query_data['UserId']}""")
        
        user_data = con.fetchone()
        if user_data == None:
            return "The UserId provided was not found, please provide a valid one"
        
        con.execute(f"select * from {SCHEMA_NAME}.book where bookid = {query_data['BookId']}")
        book_data = con.fetchone()
        if book_data == None:
            return "The BookId provided was not found, please provide a valid one"

        user_balance = float(user_data[5].replace("$", ""))
        book_price = float(book_data[4].replace("$", ""))

        if user_balance < book_price:
            return "The user doesn't have enough balance to purchase the book"


        now = datetime.datetime.now()
        con.execute(f"""insert into {SCHEMA_NAME}.purchases (UserId, BookId, PurchaseDate) 
                    values('{query_data['UserId']}', '{query_data['BookId']}', '{now}')""")
        
        con.execute(f"""update {SCHEMA_NAME}.userprofile
                        set balance = balance - {book_price}::money
                        where userid = {query_data['UserId']}
        """)

        con.execute("commit")
    except:
        con.execute("rollback")
        return "Some error has ocurred. Try again please"    
    return "Purchase created successfully"
