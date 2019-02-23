__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment2_LoadDB.py
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
cursor.execute('DROP TABLE IF EXISTS name CASCADE')
cursor.execute('DROP TABLE IF EXISTS title CASCADE')
cursor.execute('DROP TABLE IF EXISTS ratings CASCADE')
cursor.execute('DROP TABLE IF EXISTS genre CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie_genre CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie_actor CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie_writer CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie_director CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie_producer CASCADE')
cursor.execute('DROP TABLE IF EXISTS role CASCADE')
cursor.execute('DROP TABLE IF EXISTS actor_movie_role CASCADE')
cursor.execute('DROP TABLE IF EXISTS principals CASCADE')
cursor.execute('DROP TABLE IF EXISTS movie CASCADE')
cursor.execute('DROP TABLE IF EXISTS member CASCADE')
connection.commit()

# creating db tables, some are dummy tables, which will be dropped at the end,
# and also some columns will be dropped to match the schema at the end.
# print('Creating database tables...')
# cursor.execute(
#     '''CREATE TABLE name
#     (
#         nconst text PRIMARY KEY,
#         name text,
#         birthyear integer,
#         deathyear integer,
#         primaryprofession text,
#         knownfortitles text
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE title
#     (
#         tconst text PRIMARY KEY,
#         title_type text,
#         primary_title text,
#         original_title text,
#         is_adult bool,
#         start_year integer,
#         end_year integer,
#         runtime_mins integer,
#         genres text
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE ratings
#     (
#         tconst text PRIMARY KEY,
#         averageRating numeric,
#         numVotes numeric
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE principals
#     (
#       tconst text,
#       ordering text,
#       nconst text,
#       category text,
#       job text,
#       characters text
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie
#     (
#       movieid SERIAL PRIMARY KEY,
#       tconst text,
#       titleType text,
#       primaryTitle text,
#       originalTitle text,
#       startYear integer,
#       endYear integer,
#       runtimeMinutes integer,
#       averageRating numeric,
#       numVotes numeric
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE member
#     (
#       memberid SERIAL primary key,
#       nconst text,
#       name text,
#       birthYear integer,
#       deathYear integer
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE genre
#     (
#       genreid SERIAL PRIMARY KEY,
#       tconst text,
#       genres text
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie_genre
#     (
#       movieid integer references movie,
#       genreid integer references genre,
#       PRIMARY KEY (movieid, genreid)
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie_actor
#     (
#       actor integer references member,
#       movie integer references movie,
#       tconst text,
#       nconst text,
#       primary key (actor, movie)
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie_writer
#     (
#       writer integer references member,
#       movie integer references movie,
#       tconst text,
#       nconst text,
#       primary key (writer, movie)
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie_director
#     (
#       director integer references member,
#       movie integer references movie,
#       tconst text,
#       nconst text,
#       primary key (director, movie)
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE movie_producer
#     (
#       producer integer references member,
#       movie integer references movie,
#       tconst text,
#       nconst text,
#       primary key (producer, movie)
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE role
#     (
#       roleid SERIAL primary key,
#       tconst text,
#       nconst text,
#       role text
#     )'''
# )
# cursor.execute(
#     '''CREATE TABLE actor_movie_role
#     (
#       actor integer,
#       movie integer,
#       role integer,
#       primary  key (actor, movie, role)
#     )'''
# )
# connection.commit()
# # dumping tsv files to temporary tables.
# print('Importing name.basics.tsv...')
# name_basic = input("Enter filepath to name.basics.tsv...")
# with open(name_basic) as name:
#     # Omit header
#     name.readline()
#     cursor.copy_from(name, 'name')
# connection.commit()
#
# print('Importing title.basics.tsv...')
# title_basic = input("Enter filepath to title.basics.tsv...")
# with open(title_basic) as title:
#     # Omit header
#     title.readline()
#     cursor.copy_from(title, 'title')
# connection.commit()
#
# print('Importing title.ratings.tsv...')
# ratings = input("Enter filepath to title.ratings.tsv...")
# with open(ratings) as ratings:
#     # Omit header
#     ratings.readline()
#     cursor.copy_from(ratings, 'ratings')
# connection.commit()
#
# print('Importing title.principals.tsv...')
# principals = input("Enter filepath to title.principals.tsv...")
# with open(principals) as principals:
#     # Omit header
#     principals.readline()
#     cursor.copy_from(principals, 'principals')
# connection.commit()
#
# # inserting into final tables, from the temp tables
# sql_movie = 'INSERT INTO movie (tconst, titleType, primaryTitle, originalTitle, startYear, endYear, runtimeMinutes, ' \
#             'averageRating, numVotes) ' \
#              'SELECT title.tconst, title.title_type, title.primary_title, title.original_title, title.start_year, ' \
#             'title.end_year, title.runtime_mins, ratings.averageRating, ratings.numVotes\
#               FROM title \
#               FULL JOIN ratings ON title.tconst = ratings.tconst'
# print('Inserting movie...')
# cursor.execute(sql_movie)
# connection.commit()
#
# sql_genre = 'INSERT INTO genre (tconst, genres) ' \
#             'SELECT title.tconst, title.genres\
#              FROM title'
# print('Inserting genre...')
# cursor.execute(sql_genre)
# connection.commit()
#
# sql_member = 'INSERT INTO member (nconst, name, birthYear, deathYear) ' \
#              'SELECT name.nconst, name.name, name.birthyear, name.deathyear\
#               FROM name'
# print('Inserting member...')
# cursor.execute(sql_member)
# connection.commit()
#
# sql_movieactor = 'INSERT INTO movie_actor (actor, movie, tconst, nconst) ' \
#                  'SELECT distinct memberid, movieid, principals.tconst, principals.nconst  \
#                   FROM principals JOIN movie ON movie.tconst = principals.tconst  \
#                   JOIN MEMBER ON MEMBER.nconst = principals.nconst WHERE category LIKE (%s)'
# sql_actor = ("actor",)
# print('Inserting actor...')
# cursor.execute(sql_movieactor, sql_actor)
# connection.commit()
#
# sql_movie_writer = 'INSERT INTO movie_writer (writer, movie, tconst, nconst) ' \
#                    'SELECT distinct memberid, movieid, principals.tconst, principals.nconst  \
#                     FROM principals JOIN movie ON movie.tconst = principals.tconst  \
#                     JOIN MEMBER ON MEMBER.nconst = principals.nconst WHERE category LIKE (%s)'
# sql_writer = ("writer",)
# print('Inserting writer...')
# cursor.execute(sql_movie_writer, sql_writer)
# connection.commit()
#
# sql_movie_director = 'INSERT INTO movie_director (director, movie, tconst, nconst) ' \
#                      'SELECT distinct memberid, movieid, principals.tconst, principals.nconst  \
#                       FROM principals JOIN movie ON movie.tconst = principals.tconst  \
#                       JOIN MEMBER ON MEMBER.nconst = principals.nconst WHERE category LIKE (%s)'
# sql_director = ("director",)
# print('Inserting director...')
# cursor.execute(sql_movie_director, sql_director)
# connection.commit()
#
# sql_movie_producer = 'INSERT INTO movie_producer (producer, movie, tconst, nconst) ' \
#                      'SELECT distinct memberid, movieid, principals.tconst, principals.nconst  \
#                       FROM principals JOIN movie ON movie.tconst = principals.tconst  \
#                       JOIN MEMBER ON MEMBER.nconst = principals.nconst WHERE category LIKE (%s)'
# sql_producer = ("producer",)
# print('Inserting producer...')
# cursor.execute(sql_movie_producer, sql_producer)
# connection.commit()
#
# sql_role = 'INSERT INTO role (tconst, nconst, role) ' \
#            'SELECT distinct principals.tconst, principals.nconst, characters\
#             FROM principals JOIN movie ON movie.tconst = principals.tconst JOIN MEMBER ON MEMBER.nconst = principals.nconst'
# print('Inserting role...')
# cursor.execute(sql_role)
# connection.commit()
#
# sql_actor_movie_role = 'INSERT INTO actor_movie_role (actor, movie, role) ' \
#                        'SELECT movie_actor.actor, movie_actor.movie, role.roleid\
#                         FROM movie_actor JOIN role ON (movie_actor.tconst = role.tconst AND movie_actor.nconst = role.nconst)'
# print('Inserting actor_movie_role...')
# cursor.execute(sql_actor_movie_role)
# connection.commit()
#
# sql_movie_genre = 'INSERT INTO movie_genre (movieid, genreid) ' \
#                   'SELECT distinct movie.movieid, genre.genreid\
#                    FROM movie JOIN genre ON movie.tconst = genre.tconst'
# print('Inserting movie_genre...')
# cursor.execute(sql_movie_genre)
# connection.commit()
#
# # deleting and removing unwanted tables and columns from the DB to match the schema
# print("Deleting Temp tables")
# cursor.execute('DROP TABLE IF EXISTS name CASCADE')
# cursor.execute('DROP TABLE IF EXISTS title CASCADE')
# cursor.execute('DROP TABLE IF EXISTS ratings CASCADE')
# cursor.execute('DROP TABLE IF EXISTS principals CASCADE')
# cursor.execute('ALTER TABLE movie DROP COLUMN tconst CASCADE')
# cursor.execute('ALTER TABLE member DROP COLUMN nconst CASCADE')
# cursor.execute('ALTER TABLE genre DROP COLUMN tconst CASCADE')
# cursor.execute('ALTER TABLE movie_actor DROP COLUMN tconst, DROP COLUMN nconst')
# cursor.execute('ALTER TABLE movie_writer DROP COLUMN tconst, DROP COLUMN nconst')
# cursor.execute('ALTER TABLE movie_director DROP COLUMN tconst, DROP COLUMN nconst')
# cursor.execute('ALTER TABLE movie_producer DROP COLUMN tconst, DROP COLUMN nconst')
# cursor.execute('ALTER TABLE role DROP COLUMN tconst, DROP COLUMN nconst')
# connection.commit()
#
# # print out the time lapse.
# print()
# print('Done.\n Executed in (sec):', time.time() - st)