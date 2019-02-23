__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment2_LoadDB.py
"""

# A python program to create indexes of the tables.
import psycopg2

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
# a db connection variable
cursor = connection.cursor()
# creating table indexes.
print('Creating table indexes...')
cursor.execute('CREATE INDEX idx_movieid ON movie (movieid)')
cursor.execute('CREATE INDEX idx_name ON member (name)')
cursor.execute('CREATE INDEX idx_originaltitle ON movie (originaltitle)')
cursor.execute('CREATE INDEX idx_startyear ON movie (startyear)')
cursor.execute('CREATE INDEX idx_deathyear ON member (deathyear)')
cursor.execute('CREATE INDEX idx_role ON role (role)')
cursor.execute('CREATE INDEX idx_genre ON genre (genres)')
cursor.execute('CREATE INDEX idx_memberid ON member (memberid)')
cursor.execute('CREATE INDEX idx_genreid ON genre (genreid)')
cursor.execute('CREATE INDEX idx_roleid ON role (roleid)')
cursor.execute('CREATE INDEX idx_actormovierole ON actor_movie_role (actor, movie, role)')
connection.commit()