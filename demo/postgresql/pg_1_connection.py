import psycopg2

hostname = 'localhost'
port = 5432
database = 'mydb'
user = 'myuser'
password = 'mypassword'

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host=hostname,
        port=port,
        dbname = database,
        user=user,
        password=password,
    )
    cur = conn.cursor()

    ...

    conn.commit()
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
