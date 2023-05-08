from manager.models_type import DBForeignKey, DBDatetime, DBInt
from manager.models_type import table_keys

from models.user import User
from models.book import Book

@table_keys('UserId', 'BookId')
class Purchases:
    UserId  = DBForeignKey(User, "UserId")
    BookId    = DBForeignKey(Book, "BookId")
    PurchaseDate = DBDatetime()
