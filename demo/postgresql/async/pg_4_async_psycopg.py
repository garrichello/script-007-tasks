import psycopg2
import psycopg2.extras
from pprint import pprint
from datetime import datetime
import uuid

# See https://www.psycopg.org/docs/extras.html#uuid-data-type
psycopg2.extras.register_uuid()

hostname = 'localhost'
port = 5432
database = 'mydb'
user = 'myuser'
password = 'mypassword'

conn = None
cur = None

try:
    conn = psycopg2.connect(host=hostname,
                            port=port,
                            dbname=database,
                            user=user,
                            password=password,
                            async)
    cur = conn.cursor()
    conn.autocommit = True

    # Delete previous data if schema was changed
    cur.execute("drop table if exists employee")

    # Prepare database
    create_query = """
create table if not exists employee (
    id uuid primary key,
    name varchar(20) not null,
    salary int,
    hiredate timestamp
)
"""
    cur.execute(create_query)

    # Delete previous data
    # cur.execute("truncate table employee")

    # Insert single data
    insert_query = """
insert into employee (id, name, salary, hiredate)
values (%s, %s, %s, %s)
"""
    insert_values = (str(uuid.uuid4()), 'Maxim', 100, datetime.now())
    cur.execute(insert_query, insert_values)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
