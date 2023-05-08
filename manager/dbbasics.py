from manager.connection import connect, SCHEMA_NAME
from manager.models_type import _DBBasicType

def get_cloumns_and_values(obj, ignore_keys=True):
    columns = []
    values = []
    
    vals = vars(obj)
    for val_name, val_value in vals.items():
        if not issubclass(type(val_value), _DBBasicType):
            continue

        if ignore_keys and val_name in obj._multiple_keys:
            continue
        
        columns.append(val_name)
        values.append(f"\'{val_value.value}\'")
    
    return columns, values

# todo, exclude the commit here to outside the save function
def add(obj, ignore_keys=True):
    table_name = f"{SCHEMA_NAME}.{type(obj).__name__}"
    cols, vals = get_cloumns_and_values(obj, ignore_keys=ignore_keys)

    con_str = f"insert into {table_name} ( {', '.join(cols)} ) values ( { ', '.join(vals) } )"

    # print('>\n', con_str, '\n')

    con = connect()
    con.execute(con_str)
    con.execute("COMMIT")

def add_from_dict(_dict, table_name):
    columns = ', '.join(name for name, _ in _dict.items())
    values  = ', '.join(f"'{val}'" if type(val) == str else val for _, val in _dict.items())

    con_str = f"insert into {SCHEMA_NAME}.{table_name} ( {columns} ) values ( { values } )"

    # print('>\n', con_str, '\n')

    con = connect()
    con.execute(con_str)
    con.execute("COMMIT")

def update(obj):
    pass

def delete(obj):
    pass 

def get(obj, ids:list):
    pass

def dict_to_dbinstance(_dict, _class):
    '''
    all attributes listed in _dict, most be a _DBBasicType in _class
    '''

    my_instance = _class()

    for name,val in _dict.items():
        wraper = getattr(my_instance, name)
        
        wraper.value = val 

        setattr(my_instance, name, wraper)
    
    return my_instance