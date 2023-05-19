from manager.models_type import DBInt, DBFloat
from manager.models_type import DBMoney, DBDatetime, DBForeignKey
from manager.models_type import table_keys

from models.user import User
from models.book import Book

@table_keys('DMId')
class DataMart:
    DMId = DBInt(autogenerated=True)
    UserId = DBForeignKey(User, "UserId")
    BookId = DBForeignKey(Book, "BookId")
    DateTime = DBDatetime()
    Price = DBMoney()
    Rating = DBFloat()
    Amount_In_Cart = DBInt()
    Purchased_Amount = DBInt()
    