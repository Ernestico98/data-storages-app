from manager.models_type import DBIntKey, DBVarchar

class Publisher:
    PublisherId = DBIntKey()
    Country = DBVarchar(max_len=60)
    Name = DBVarchar()
