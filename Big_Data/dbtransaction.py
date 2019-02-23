__author__ = 'BR'

"""
Author: BIKASH ROY

File name: dbtransaction.py
"""


import psycopg2


def main():
    connection = psycopg2.connect(
        host='localhost',
        dbname='sample_db',
        port='5432',
        user='',
        password=''
    )

    try:
        cursor = connection.cursor()
        connection.cursor()
        sql = "INSERT INTO principals (tconst, nconst, category) VALUES (%s, %s, %s)"
        val = [
            ('tt00103', 'tt89283', 'Producer'),
            ('tt00104', 'tt89282', bool),
            ('tt00105', 'tt89284', 'Actor')
        ]

        cursor.executemany(sql, val)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    main()
