__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment3_Naive.py
"""

import sys
import psycopg2
import psycopg2.extras
import time


st = time.time()
host = input("Enter the db host name.")
dbname = input("Enter db name.")
port = input("Enter port number to connect to db")
user = input("Enter username.")
password = input("Enter password")
# make connection to the database
connection = psycopg2.connect(
    host=host,
    dbname=dbname,
    port=port,
    user=user,
    password=password
)


# Get the column names of the table
def get_column_names(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = \'movie_all\'')
    result = cursor.fetchall()
    if not result:
        raise psycopg2.Error(f'Table movie_all couldn\'t be found.')
    fields = []

    for row in result:
        field = row[0]
        fields.append(field)
    return fields


# Get the functional dependency
def get_functional_dependency(connection):
    fields = get_column_names(connection)
    cursor = connection.cursor()
    print(f'\nNow analyzing table movie_all...')
    func_depends = []
    # Find for single attributes
    for i in range(0, len(fields)):
        for j in range(len(fields)):
            if i == j:
                continue
            field_1 = fields[i]
            field_2 = fields[j]
            cursor.execute(
                f'SELECT {field_1}, COUNT(DISTINCT {field_2}) FROM movie_all GROUP BY {field_1} '
                f'HAVING COUNT(DISTINCT {field_2}) > 1')
            if cursor.rowcount == 0:
                func_depends.append(f'{field_1} -> {field_2}')
    # Find for double attributes
    for i in range(0, len(fields)):
        for j in range(len(fields)):
            for k in range(len(fields)):
                if i == j == k:
                    continue
                field_1 = fields[i]
                field_2 = fields[j]
                field_3 = fields[k]
                cursor.execute(
                    f'SELECT {field_1}, {field_2}, COUNT(DISTINCT {field_3}) FROM movie_all '
                    f'GROUP BY {field_1}, {field_2} '
                    f'HAVING COUNT(DISTINCT {field_3}) > 1')
                if cursor.rowcount == 0:
                    func_depends.append(f'{field_1}, {field_2} -> {field_3}')
    # Print results
    print('Results for movie_all')
    if func_depends:
        print('Following functional dependencies found:')
        for fd in func_depends:
            print(fd)
    else:
        print('No functional dependencies found.')


try:
    get_functional_dependency(connection)

except psycopg2.Error as err:
    sys.exit(f'An error occurred:\n{err}\nExiting...')

finally:
    connection.close()
print('Done.\n Executed in (sec):', time.time() - st)
