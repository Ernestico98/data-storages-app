from manager.models_type import DBForeignKey, DBInt, DBVarchar
from manager.models_type import table_keys

from models.user import User
from models.book import Book

@table_keys('UserId', 'BookId')
class Reviews:
    UserId  = DBForeignKey(User, "UserId")
    BookId  = DBForeignKey(Book, "BookId")
    Rating  = DBInt(not_null=True)
    Comment = DBVarchar()
