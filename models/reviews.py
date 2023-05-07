from manager.models_type import DBForeignKey, DBInt, DBVarchar
from manager.models_type import table_keys

from models.author import Author
from models.book import Book

@table_keys('UserId', 'BookId')
class Reviews:
    UserId  = DBForeignKey(Author, "AuthorId")
    BookId  = DBForeignKey(Book, "BookId")
    Rating  = DBInt(not_null=True)
    Comment = DBVarchar()
