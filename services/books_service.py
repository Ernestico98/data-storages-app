from manager.connection import connect, SCHEMA_NAME, connect_rc
from prettytable import PrettyTable
from utils import datetime_deserializer, datetime_serializer
import json


def get_books_by_author( query_data ):
    con = connect()
    rc = connect_rc()
    
    cache_str = f"{SCHEMA_NAME}_CACHE_get_books_by_author_{query_data['FirstName'].lower()}_{query_data['LastName'].lower()}"
    if rc.exists(cache_str):
        print('Is in cache')
        res = json.loads(rc.get(cache_str), object_hook=datetime_deserializer)
    else:
        print('Is not in cache')
        con.execute(f"""select b.bookid , b.title, b.publishdate, b.price from {SCHEMA_NAME}.book b 
            inner join {SCHEMA_NAME}.writenby w on b.bookid = w.bookid
            inner join {SCHEMA_NAME}.author a on w.authorid = a.authorid
            where lower(a.firstname) like '%{query_data['FirstName'].lower()}%'
            and lower(a.lastname) like '%{query_data['LastName'].lower()}%'
        """)
        res = con.fetchall()
        rc.set(cache_str, json.dumps(res, default=datetime_serializer))
    
    table = PrettyTable()
    table.field_names = ["BookId", "Title", "Publish Date", "Price"]
    for row in res:
        table.add_row(row)
    
    return table

def create_book( query_data ):
    try:
        con = connect()
        rc = connect_rc()

        con.execute(f"select PublisherId from {SCHEMA_NAME}.publisher where publisherid = {query_data['PublisherId']}")
        pid = con.fetchone()
        
        if pid == None:
            return "The PublisherId provided was not found, please provide a valid one"
        author_ids = [str(i) for i in query_data['AuthorIds']]
        #print(','.join(query_data['AuthorIds']))
        author_ids_list = ','.join(author_ids)
        
        con.execute(f"""select count(*) 
                        from {SCHEMA_NAME}.author 
                        where authorid in ({author_ids_list})""")

        count = int(con.fetchone()[0])
        
        if count != len(author_ids):
            return "There is/are {count} author that are not registered in the system. Please register them and try again"
        
        
        con.execute(f"""insert into {SCHEMA_NAME}.book (Title, CoverImage, PublishDate, Price, PublisherId) 
                    values('{query_data['Title']}', '{query_data['CoverImage']}', '{query_data['PublishDate']}',
                    '{query_data['Price']}', '{query_data['PublisherId']}') RETURNING BookId""")

        book_id = con.fetchone()[0]

        for author_id in query_data['AuthorIds']:
            con.execute(f"""
                insert into {SCHEMA_NAME}.writenby (authorid, bookid)
                values ({author_id}, {book_id})
            """)
            
            # invalidate get_books_by_author cache
            con.execute(f"""select FirstName, LastName from {SCHEMA_NAME}.author where AuthorId='{author_id}'""")
            firstName, lastName = con.fetchone()
            cache_str = f"{SCHEMA_NAME}_CACHE_get_books_by_author_{firstName.lower()}_{lastName.lower()}"
            rc.delete(cache_str)
            

        con.execute('commit')
    except Exception as exception:
        print(exception)
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

def set_book_review( query_data:dict ):
    try:
        con = connect()
        rc = connect_rc()

        userid = int(query_data["UserId"])
        bookid = int(query_data["BookId"])
        rating = int(query_data["Rating"])
        comment = query_data.get("Comment", '')

        assert rating >= 0 and rating <= 5, "Rating must be in the range [0,5]"
        
        con.execute(f"""insert into {SCHEMA_NAME}.reviews (UserId, BookId, Rating, Comment) 
                    values('{userid}', '{bookid}', '{rating}', '{comment}')""")

        # redis cache for the reviews   
        var_name = f"{SCHEMA_NAME}_reviewmean_{bookid}"
        value = rc.get(var_name)
        value = value.decode() if value is not None else "0:0"
        value = value.split(":")

        sum_, ctn_ = int(value[0]), int(value[1])

        sum_ += rating
        ctn_ += 1 

        value = f"{sum_}:{ctn_}"
        
        rc.set(var_name, value)

        con.execute('commit')

    except Exception as exception:
        print(exception)
        con.execute("rollback")
        return "Some error has ocurred. Try again please"

    return "Review created successfully"
    