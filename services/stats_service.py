from manager.connection import connect_rc, connect, SCHEMA_NAME
from prettytable import PrettyTable

def get_purchases_book_stats(args):
    rc = connect_rc()

    table = PrettyTable()
    table.field_names = ["BookId", "InCart", "Purchases"]

    info = {}
    keys = rc.keys('*_stbookbuy_*')
    offset = len(SCHEMA_NAME) + len('_stbookbuy_')

    for key in keys:
        val = int(rc.get(key))
        ide = int(key[offset:])

        info.update({ide:[0,val]})

    keys = rc.keys('*_stbookcart_*')
    offset = len(SCHEMA_NAME) + len('_stbookcart_')

    for key in keys:
        val = rc.get(key)
        ide = int(key[offset:])

        try:
            cv = info[ide]
        except:
            cv = [0,0]
        
        cv[0] = int(val)
        info.update({ide:cv})
    
    for key, value in info.items():
        table.add_row([key, value[0], value[1]])

    return table

def reset_stats(args):
    try:
        con = connect()
        con.execute(f"""select p.bookid , count(*) as total  
                        from {SCHEMA_NAME}.purchases p 
                        group by p.bookid""")
        pairs = con.fetchall()
        del con 

        rc = connect_rc()
        for bookid, total in pairs: 
            value_key = f"{SCHEMA_NAME}_stbookbuy_{bookid}"
            rc.set(value_key, total)
    except Exception as e:
        error_message = str(e)
        return f"Some error has occurred. Error message: {error_message}"

    return "Statistics were recalculated correctly."