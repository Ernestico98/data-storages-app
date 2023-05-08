from manager.models_type import _DBBasicType
from manager.connection import connect, SCHEMA_NAME
from manager.model_list import MODELS

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
        
        # add multiple keys constraign
        try:
            mk = _class._multiple_keys
        except:
            mk = []
        
        if len(mk) > 0:
            atributes.append(f"PRIMARY KEY ({sep.join(mk)})")

        print (f'# Start table {name} setup')

        create_string = f"create table if not exists {name}( {sep.join(atributes)} )"
        
        # print('>\n', create_string, '\n')

        con.execute(create_string)

        print(' Done')

    
    con.execute("COMMIT")

