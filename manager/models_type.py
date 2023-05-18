import datetime
from datetime import timezone
from manager.connection import SCHEMA_NAME

class _DBBasicType:
    create_string = ""
    base_type = None

    def make_type_string(self):
        return self.create_string

class DBInt(_DBBasicType):
    create_string = ""
    base_type = 'int'
    value = 0

    def __init__(self, default=0, not_null=False, autogenerated=False) -> None:
        self.value = default

        not_null = " NOT NULL" if not_null else " "
        end_string = " GENERATED ALWAYS AS IDENTITY" if autogenerated else f"DEFAULT {default}{not_null}"

        self.create_string = f"int {end_string}"

class DBFloat(_DBBasicType):
    create_string = ""
    base_type = 'float'
    value = 0.0

    def __init__(self, default=0.0, not_null=False) -> None:
        self.value = default

        not_null = " NOT NULL" if not_null else " "
        end_string = f"DEFAULT {default}{not_null}"

        self.create_string = f"float {end_string}"
    
class DBVarchar(_DBBasicType):
    value = ""
    create_string = ""
    base_type = 'varchar'

    def __init__(self, default="", max_len=None, not_null=False) -> None:
        self.value = default
        
        the_type = "varchar" if max_len is None else f"varchar({max_len})"
        not_null = " NOT NULL" if not_null else " "

        self.create_string = f"{the_type} DEFAULT '{default}'{not_null}"

class DBMoney(_DBBasicType):
    create_string = ""
    value = 0
    base_type = 'money'

    def __init__(self, default=0, not_null=False) -> None:
        self.value = default

        not_null = " NOT NULL" if not_null else " "

        self.create_string = f"money DEFAULT {default} {not_null}"

class DBDate(_DBBasicType):
    create_string = ""
    value = 0
    base_type = 'date'

    def __init__(self, default=datetime.datetime.today(), not_null=False) -> None:
        self.value = default

        not_null = "NOT NULL" if not_null else " "
        default = default.strftime("%Y-%m-%d")

        self.create_string = f"date DEFAULT \'{default}\' {not_null}"

class DBDatetime(_DBBasicType):
    create_string = ""
    value = 0
    base_type = 'date'

    def __init__(self, default=datetime.datetime.now(timezone.utc), not_null=False) -> None:
        self.value = default

        not_null = "NOT NULL" if not_null else " "
        default = default.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'

        self.create_string = f"timestamp DEFAULT \'{default}\' {not_null}"

class DBForeignKey(_DBBasicType):
    create_string = ""

    def __init__(self, table:_DBBasicType, column:str) -> None:
        table_name = f"{SCHEMA_NAME}.{table.__name__}"

        # find column
        vals = vars(table)
        for val_name, val_value in vals.items():
            if val_name == column:
                assert issubclass(type(val_value), _DBBasicType), "the foreign attribute must be a sub class of _DBBasicType"
                assert val_value.base_type is not None, "table basic_type must be not None"
                
                self.base_type = val_value.base_type

                self.create_string = f"{self.base_type} REFERENCES {table_name}({val_name})"

def table_keys(*key_list):
    def decorator(cls):
        cls._multiple_keys = key_list
        return cls
    return decorator
