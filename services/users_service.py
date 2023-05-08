from manager.connection import connect, SCHEMA_NAME
from prettytable import PrettyTable


def create_user( query_data ):
    con = connect()
    con.execute(f"""insert into bookstoreschema.user (email, password, role) 
                    values('{query_data['Email']}', '{query_data['Password']}', '{query_data['Role']}')""")
    
    con.execute('commit')
    
    return "User created successfully"