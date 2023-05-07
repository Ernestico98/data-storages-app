from manager.models_type import DBIntKey, DBVarchar

class Author:
    AuthorId = DBIntKey()
    FirstName = DBVarchar(max_len=50, not_null=True)
    LastName = DBVarchar(max_len=50)
