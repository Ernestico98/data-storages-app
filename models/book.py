from manager.models_type import DBIntKey, DBVarchar
from manager.models_type import DBMoney, DBDate, DBForeignKey

from models.publisher import Publisher

class Book:
    BookId = DBIntKey()
    Title = DBVarchar(max_len=250, not_null=True)
    CoverImage = DBVarchar(max_len=500)
    PubishDate = DBDate()
    Price = DBMoney()
    PublisherId = DBForeignKey(Publisher, "PublisherId")
