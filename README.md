# data-storages-app
Project for Data Storages Course

## Install
Create environment
```
python -m venv .venv
source .venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

Configure the Enviroment variables. For development stage, you can use an .env file:

```
cp .env.example .env
```

then fill each variable with its true value ;)

## Models
Create a model class in some file within the folder models like this:

```python
from manager.models_type import *

@table_keys('PublisherId')
class Publisher:
    PublisherId = DBInt(autogenerated=True)
    Name = DBVarchar()
```

### Setup Models

The folowing command will create and populate all tables. If they are already created, they will be delet it first.

```shell
python main.py --setup
```

### Query by command line
Use -q and -d parameters like this

```shell
python main.py -q get_purchases_by_user -d "{\"UserId\":2}"
```

-q is the query name
-d the data in json format

for more information use --help

### Available queries
- -q get_purchases_count
- -q get_purchases_by_user -d '{\"UserId\" : 1}'
- -q get_books_by_author -d '{\"FirstName\" : \"John\", \"LastName\" : \"Doe\"}'
- -q create_user -d '{\"Email\" : \"test@email.com\", \"Password\" : \"password\", \"Role\" : \"admin\"}'
- -q create_book -d '{\"PublisherId\" : 1, \"AuthorIds\" : [1], \"Title\" : \"Title\", \"CoverImage\" : \"Path/to/image\", \"PublishDate\" : \"2023-02-01\", \"Price\" : 123}'
- -q create_purchase -d '{\"UserId\" : 1, \"BooksIds\" : [1, 2]}'
- -q get_total_sales_by_book
- -q get_top_10_books_by_avg_rating
- -q add_to_cart -d '{\"UserId\" : 1, \"BookId\" : 1}'
- -q remove_from_cart -d '{\"UserId\" : 1, \"BookId\" : 1}'
- -q clear_cart -d '{\"UserId\" : 1}'
- -q purchase_from_cart -d '{\"UserId\" : 1}'
- -q get_cart_contents -d '{\"UserId\" : 1}'
- -q set_book_review -d '{\"UserId\" : 1, \"BookId\" : 1, \"Comment\" : \"\", \"Rating\" : 5}'

### Anlalytical queries using DataMart
- -q top_ten_users_by_purchases
- -q total_revenue_per_book
- -q total_revenue__vs_rating

### Managing high RPS using redis
#### Scenario 1: "Creation of shoping cart"

There were 5 methods (add_to_cart, remove_from_cart, clear_cart, purchase_from_cart, get_cart_contents) implemented to support this functionality. Basically a unique key ("{SCHEMA}\_shop_cart\_{UserId}") is assigned to each user to store a set of ids of books in the user's cart.


In addition, a general statistic of the status of book sales can be obtained with the method:

- -q get_purchases_book_stats
- -q reset_stats

It returns how many times a book was purchased for each book, and what quantity is still in the cart. The second, slower version, recalculates the statistics and stores them in reedis as a cache.

In set_book_review function, it is kept with the key: 
"{SCHEMA_NAME}_reviewmean_{BookId}"
a chain that representing "{first number}:{second number}".
The first number is the sum of the book reviews and the second is the number of reviews of that book, which will be used by other processes to quickly calculate the average rating.

#### Scenario 2: "Caching some SQL queries"
- `get_books_by_author`: Cache SQL query to get the books per author.
- `create_book`: Invalidates prevoius cache for corresponding authors.
- `get_purchases_by_user`: Cache SQL query to get the purchases made by an user.
- `create_purchase`: Invalidates previous cache for corresponding user making purchase.  
