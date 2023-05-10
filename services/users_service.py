from manager.connection import connect, SCHEMA_NAME
from prettytable import PrettyTable


def create_user( query_data ):
    try:

        con = connect()
        con.execute(f"""insert into bookstoreschema.user (email, password, role) 
                        values('{query_data['Email']}', '{query_data['Password']}', '{query_data['Role']}')""")
        
        con.execute('commit')
    except:
        con.execute("rollback")
        return "Some error has ocurred. Try again please"
    
    return "User created successfully"