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
    conn = psycopg2.connect(
        host=hostname,
        port=port,
        dbname=database,
        user=user,
        password=password,
    )
    # cur = conn.cursor()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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

    # Insert multiple data
    # https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
    insert_values = [
        (str(uuid.uuid4()), 'Tanya', 110, datetime.now()),
        (str(uuid.uuid4()), 'Stefan', 200, datetime.now()),
        (str(uuid.uuid4()), 'Eugene', 150, datetime.now()),
        (str(uuid.uuid4()), 'Alex', 250, datetime.now()),
    ]
    insert_query = "insert into employee (id, name, salary, hiredate) values %s"
    psycopg2.extras.execute_values(cur, insert_query, insert_values)

    # Update
    update_query = 'update employee set salary=salary+10'
    cur.execute(update_query)

    # Delete
    delete_query = 'delete from employee where name=%s'
    delete_record = ('Maxim',)
    cur.execute(delete_query, delete_record)

    # fetchone
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchone
    print('\n--- Using fetchone\n')
    cur.execute('select * from employee')
    record = cur.fetchone()
    print(record[0], record[1])

    # fetchmany
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchmany
    print('\n--- Using fetchmany\n')
    cur.execute('select * from employee')
    while records := cur.fetchmany(2):
        print('-')
        for record in records:
            print(record[0], record[1])

    # fetchall
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchall
    print('\n--- Using fetchall\n')
    cur.execute('select * from employee')
    for record in cur.fetchall():
        print(record[0], record[1])

    # mix it up
    print('\n--- Using fetch*\n')
    cur.execute('select * from employee')
    record = cur.fetchone()
    print(record)
    for record in cur.fetchmany(2):
        print(record)
    for record in cur.fetchall():
        print(record)

    # Select as dict (requires cursor_factory=psycopg2.extras.DictCursor)
    print('\n--- Select using named results\n')
    cur.execute('select * from employee')
    for record in cur.fetchall():
        print(record['name'], record['salary'])

    # Prepare statement dynamically
    # avoiding SQL injection
    print('\n--- Dynamic statement\n')
    columns = ('name', 'salary')
    select_query = psycopg2.sql.SQL('select {} from {}').format(
        psycopg2.sql.SQL(',').join(map(psycopg2.sql.Identifier, columns)),
        psycopg2.sql.Identifier('employee'))
    cur.execute(select_query)
    for record in cur.fetchall():
        print(record)

    # Use postional params
    # (actually the same as above for other queries)
    print('\n--- Positional params\n')
    cur.execute('select * from employee where name=%s', ('Stefan',))
    for record in cur.fetchall():
        print(record[0], record[1])

    # Use named params
    print('\n--- Named params\n')
    cur.execute('select * from employee where name=%(name)s',
                {'name': 'Stefan'})
    for record in cur.fetchall():
        print(record[0], record[1])

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
