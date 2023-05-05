from manager.models_type import parse_type_to_db

#*****************************************************
# Here you inscribe your models

from models.books import Books

# Model list
MODELS = [
    Books,
]


#*****************************************************

def setup_models():
    sep = ', '

    for _class in MODELS:
        name = _class.__name__
        atributes = []

        vals = _class.__annotations__
        for val_name, val_value in vals.items():
            the_type = parse_type_to_db(val_value)
            atributes.append(f"{val_name} {the_type}")
        
        # create table with name 
        # add atributes

        create_string = f"create table if not exists {name}( {sep.join(atributes)} )"
        
        # add conection and run the query
        print (create_string)

