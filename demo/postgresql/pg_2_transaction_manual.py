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
        dbname=database,
        user=user,
        password=password,
    )

    # Transaction is automatically created
    cur = conn.cursor()

    cur.execute("drop table if exists employee")
    cur.execute("""
create table if not exists employee (
    id int primary key,
    name varchar(20) not null,
    salary int
)
""")
    insert_query = "insert into employee (id, name, salary) values (%s, %s, %s)"
    cur.execute(insert_query, (1, 'Maxim', 100))
    cur.execute(insert_query, (2, 'Tanya', 200))
    cur.execute(insert_query, (3, 'Stefan', 300))

    conn.commit()  # needed to write results to database
    # conn.rollback()  # revert all changes
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
