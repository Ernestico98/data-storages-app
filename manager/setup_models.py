from manager.models_type import _DBBasicType
from manager.connection import connect, SCHEMA_NAME

#*****************************************************
# Here you inscribe your models

from models.book import Book
from models.publisher import Publisher
from models.author import Author

# Model list
MODELS = [
    Publisher,
    Author,
    Book,
]

#*****************************************************

def setup_models():
    sep = ', '

    con = connect()
    con.execute(f"create schema if not exists {SCHEMA_NAME}")

    for _class in MODELS:
        name = f"{SCHEMA_NAME}.{_class.__name__}"
        atributes = []

        vals = vars(_class)

        for val_name, val_value in vals.items():
            if not issubclass(type(val_value), _DBBasicType):
                continue
            
            the_type = val_value.make_type_string()
            atributes.append(f"{val_name} {the_type}")
        
        # create table with name 
        # add atributes

        create_string = f"create table if not exists {name}( {sep.join(atributes)} )"
        
        # print('>\n', create_string, '\n')

        con.execute(create_string)
    
    con.execute("COMMIT")

