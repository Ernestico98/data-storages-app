from manager.models_type import DBInt, DBVarchar, DBForeignKey, DBMoney
from manager.models_type import table_keys

from models.user import User

@table_keys('UserProfileId')
class UserProfile:
    UserProfileId = DBInt(autogenerated=True)
    Balance = DBMoney()
    ProfilePicture = DBVarchar(max_len=500)
    Country = DBVarchar(max_len=60)
    NickName = DBVarchar(max_len=100, not_null=True)
    FullName = DBVarchar(max_len=250, not_null=True)
    Description = DBVarchar(max_len=500)
    UserId = DBForeignKey(User, "UserId")
