from manager.connection import connect, SCHEMA_NAME
from prettytable import PrettyTable


def get_books_by_author( query_data ):
    con = connect()
    con.execute(f"""select b.bookid , b.title, b.publishdate, b.price  from {SCHEMA_NAME}.book b 
                    inner join {SCHEMA_NAME}.author a  on b.authorid  = a.authorid 
                    where a.firstname = '{query_data['FirstName']}' and a.lastname = '{query_data['LastName']}'
                """)
    
    table = PrettyTable()
    table.field_names = ["BookId", "Title", "Publish Date", "Price"]
    res = con.fetchall()
    for row in res:
        table.add_row(row)
    
    return table

def create_book( query_data ):

    try:
        con = connect()

        con.execute(f"select PublisherId from {SCHEMA_NAME}.publisher where publisherid = {query_data['PublisherId']}")
        pid = con.fetchone()
        if pid == None:
            return "The PublisherId provided was not found, please provide a valid one"
        
        con.execute(f"select AuthorId from {SCHEMA_NAME}.author where authorid = {query_data['AuthorId']}")
        aid = con.fetchone()
        if aid == None:
            return "The AuthorId provided was not found, please provide a valid one"
        
        con.execute(f"""insert into {SCHEMA_NAME}.book (Title, CoverImage, PublishDate, Price, PublisherId, AuthorId) 
                    values('{query_data['Title']}', '{query_data['CoverImage']}', '{query_data['PublishDate']}', '{query_data['Price']}', '{query_data['PublisherId']}', '{query_data['AuthorId']}')""")
        con.execute('commit')
    except:
        con.execute("rollback")
        return "Some error has ocurred. Try again please"
    return "Book created successfully"

def get_total_sales_by_book( query_data ):
    con = connect()

    con.execute(f"""select b.bookid , b.title , b.publishdate, b.price , count(*) as total_sales  
                    from {SCHEMA_NAME}.book b 
                    join {SCHEMA_NAME}.purchases p  on b.bookid  = p.bookid
                    group by 1,2,3,4
                    order by 5 desc""")

    table = PrettyTable()
    table.field_names = ["BookId", "Title", "Publish Date", "Price", "Total Sales"]
    res = con.fetchall()
    for row in res:
        table.add_row(row)

    return table

def get_top_10_books_by_avg_rating( query_data ):
    con = connect()

    con.execute(f"""select b.bookid , b.title , b.publishdate, b.price , avg(r.rating) as avg_rating  
                    from {SCHEMA_NAME}.book b 
                    join {SCHEMA_NAME}.reviews r  on b.bookid  = r.bookid
                    group by 1,2,3,4
                    order by 5 desc
                    limit 10""")

    table = PrettyTable()
    table.field_names = ["BookId", "Title", "Publish Date", "Price", "Average Rating"]
    res = con.fetchall()
    for row in res:
        table.add_row(row)

    return table