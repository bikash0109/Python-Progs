__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment3_CreateTable.py
"""
# a python program to load the data into database from TSV files.
import psycopg2
import time

# start logging time
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
# a db connection variable
cursor = connection.cursor()

# deleting any old tables existing of same name
print('Dropping old database tables...')
cursor.execute('DROP TABLE IF EXISTS movie_all CASCADE')

# creating new table
print('Creating database tables...')
cursor.execute(
    '''CREATE TABLE movie_all
    (
      movieid integer,
      type text,
      startYear integer,
      runtime integer,
      avgRating numeric,
      genreid integer,
      genre text,
      memberid integer,
      birthYear integer,
      role integer primary key
    )'''
)

connection.commit()

# inserting into final tables, after joining the 5 tables
sql_movie = 'INSERT INTO movie_all (movieid, type, startYear, runtime, avgRating, genreid, genre, ' \
            'memberid, birthYear, role) ' \
            'SELECT movie.movieid, titletype, startyear, runtimeMinutes, averageRating, genre.genreid, genres,' \
            'memberid, birthYear, role\
             FROM movie \
             JOIN actor_movie_role ON actor_movie_role.movie = movie.movieid \
             JOIN member on member.memberid = actor_movie_role.actor ' \
            'JOIN movie_genre on movie_genre.movieid = movie.movieid ' \
            'JOIN genre on genre.genreid = movie_genre.genreid ' \
            'JOIN movie_actor on movie_actor.actor = member.memberid ' \
            'WHERE runtimeMinutes > 90 ' \
            'GROUP BY movie.movieid, genre.genreid, memberid, actor_movie_role.role ' \
            'HAVING count(role) = 1' \

print('Inserting movie...')
cursor.execute(sql_movie)
connection.commit()
print()
print('Done.\n Executed in (sec):', time.time() - st)