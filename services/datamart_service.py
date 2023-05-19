from manager.connection import connect, SCHEMA_NAME, connect_rc
import datetime
from prettytable import PrettyTable
import json
from utils import datetime_deserializer, datetime_serializer
import matplotlib.pyplot as plt

def top_ten_users_by_purchases( query_data ):
    con = connect()
    con.execute(f"""SELECT userid, COUNT(*) AS total_purchases
                    FROM {SCHEMA_NAME}.datamart
                    GROUP BY userid
                    ORDER BY total_purchases DESC
                    LIMIT 10""")
    
    data = con.fetchall()

    user_ids = [i[0] for i in data]
    total_purchases  = [i[1] for i in data]

    
    plt.bar(user_ids, total_purchases)
    plt.xlabel('User ID')
    plt.ylabel('Total Purchases')
    plt.title('Total Purchases per User (Top 10)')
    plt.xticks(user_ids)

    plt.show()

def total_revenue_per_book( query_data ):
    con = connect()
    con.execute(f"""SELECT bookid, SUM(price) AS total_revenue
                    FROM {SCHEMA_NAME}.datamart
                    GROUP BY bookid
                    ORDER BY total_revenue DESC;""")
    
    data = con.fetchall()

    book_ids = [i[0] for i in data]
    total_revenue  = [i[1] for i in data]

    
    plt.bar(book_ids, total_revenue)
    plt.xlabel('Book ID')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue Per Book')
    plt.xticks(book_ids)

    plt.show()

def correlation_total_revenue_rating( query_data ):
    con = connect()
    con.execute(f"""SELECT d.bookid, total_revenue, avg_rating
                    FROM (
                        SELECT SUM(price) AS total_revenue, bookid
                        FROM {SCHEMA_NAME}.datamart
                        GROUP BY bookid
                    ) d
                    INNER JOIN (
                        SELECT AVG(rating) AS avg_rating, bookid
                        FROM {SCHEMA_NAME}.reviews
                        GROUP BY bookid
                    ) r ON d.bookid = r.bookid
                    order by total_revenue
                    """)
    
    results = con.fetchall()
    book_ids, revenues, ratings = zip(*results)

    book_ids = [str(i) for i in book_ids]

    plt.plot(book_ids, ratings)
    plt.xlabel('Book ID')
    plt.ylabel('Average Rating')
    plt.title('Revenue vs Rating')
    plt.xticks(book_ids)

    for i, revenue in enumerate(revenues):
        plt.text(book_ids[i], ratings[i], str(revenue), ha='center', va='bottom')


    plt.xticks(rotation=45)  

    plt.show()

