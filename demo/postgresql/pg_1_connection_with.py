import psycopg2

hostname = 'localhost'
port = 5432
database = 'mydb'
user = 'myuser'
password = 'mypassword'

try:
    with psycopg2.connect(
        host=hostname,
        port=port,
        dbname = database,
        user=user,
        password=password,
    ) as conn:

        with conn.cursor() as cur:
            ...
            # cur.close() # done automatically

        # conn.commit() # done automatically

except Exception as e:
    print(e)
finally:
    conn.close()
