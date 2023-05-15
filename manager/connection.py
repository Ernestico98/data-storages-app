import psycopg2, os, redis

SCHEMA_NAME = 'BookStoreSchema'

def connect():
    database = os.getenv('DATABASE_NAME')
    user = os.getenv('DATABASE_USER')
    password = os.getenv('DATABASE_PASSWORD')
    host = os.getenv('DATABASE_HOST')
    port = os.getenv('DATABASE_PORT')
    
    conn = psycopg2.connect(database=database, user=user,
                            password=password, host=host, port=port)
    
    return conn.cursor()

def connect_rc():
    host = os.getenv('REDIS_HOST')
    port = os.getenv('REDIS_PORT')
    pwd  = os.getenv('REDIS_PASSWORD')

    rc = redis.Redis(host=host,port=port,password=pwd) 

    return rc