from manager.connection import connect, SCHEMA_NAME

def get_purchases_count(guery_data):
    con = connect()
    con.execute(f"select count(*) from {SCHEMA_NAME}.purchases")
    
    ctn = con.fetchone()

    return ctn[0]


def get_purchases_by_user(guery_data):
    UserId = guery_data['UserId']

    con = connect()
    con.execute(f"select * from {SCHEMA_NAME}.purchases where UserId={UserId}")

    sol = con.fetchall()

    return sol
