#*****************************************************
# Here you inscribe your models

# entities
from models.book import Book
from models.publisher import Publisher
from models.author import Author
from models.user import User
from models.userprofile import UserProfile

# relationships
from models.writenby import WritenBy
from models.reviews import Reviews
from models.purchases import Purchases

#DataMart Tables
from models.datamart import DataMart


# Model list
MODELS = [
    Publisher,
    Author,
    Book,
    WritenBy,
    User,
    UserProfile,
    Reviews,
    Purchases,
    DataMart,
]

#*****************************************************
