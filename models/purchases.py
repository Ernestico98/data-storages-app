from manager.models_type import DBForeignKey
from manager.models_type import table_keys

from models.author import Author
from models.book import Book

@table_keys('UserId', 'BookId')
class Purchases:
    UserId  = DBForeignKey(Author, "AuthorId")
    BookId    = DBForeignKey(Book, "BookId")
