__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment2_LoadDB.py
"""

# A python program to run the queries and record its execution time.
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
# first query
print("(Q)2.1. Number of invalid Movie_Actor relationships with respect to roles")
st = time.time()
print("Processing ...")
question1 = 'SELECT COUNT(actor_movie_role.actor) \
FROM actor_movie_role \
JOIN (SELECT roleid FROM role WHERE role IS null) AS ro \
ON actor_movie_role.role = ro.roleid'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)

# second query
print("\n*************************************************************************\n")
print("(Q)2.2. Alive actors whose name starts with “Phi” and did not participate in any movie in 2014")
st = time.time()
print("Processing ...")
question1 = 'SELECT DISTINCT name \
             FROM movie_actor \
             JOIN (SELECT memberid, name FROM MEMBER WHERE name LIKE \'Phi%\' AND deathyear IS null) AS mem \
             ON mem.memberid = movie_actor.actor \
             JOIN (SELECT movieid FROM movie WHERE startyear <> 2014) AS mov \
             ON mov.movieid = movie_actor.movie'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)

# third query
print("\n*************************************************************************\n")
print("(Q)2.3. Producers who have produced more than 50 talk shows in 2017 and whose name contains “Gill”")
st = time.time()
print("Processing ...")
question1 = 'SELECT name \
FROM movie_producer \
JOIN movie_genre ON movie_genre.movieid = movie_producer.movie \
JOIN (SELECT genreid FROM genre WHERE genres = \'Talk-Show\')AS gen \
ON gen.genreid = movie_genre.genreid \
JOIN (SELECT memberid, name FROM MEMBER WHERE name LIKE \'%Gill%\')AS mem \
ON mem.memberid = movie_producer.producer \
GROUP BY name HAVING count(name) > 50'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)

# fourth query
print("\n*************************************************************************\n")
print("(Q)2.4. Average runtime for movies whose original title contain “Bhardwaj” and "
      "were written by somebody who is still alive.")
st = time.time()
print("Processing ...")
question1 = 'SELECT AVG(runtimeminutes) \
FROM movie_writer \
JOIN (SELECT memberid FROM MEMBER WHERE deathyear IS null) AS mem \
ON mem.memberid = movie_writer.writer \
JOIN (SELECT movieid, runtimeminutes FROM movie WHERE originaltitle LIKE \'%Bhardwaj%\')AS mov \
ON mov.movieid = movie_writer.movie'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)

# fifth query
print("\n*************************************************************************\n")
print("(Q)2.5. Alive producers with the greatest number of long-run movies produced(runtime greater than 120 minutes)")
st = time.time()
print("Processing ...")
question1 = 'SELECT DISTINCT name \
FROM movie_producer \
JOIN (SELECT memberid, name FROM MEMBER WHERE deathyear IS null) AS mem \
ON mem.memberid = movie_producer.producer \
JOIN (SELECT movieid FROM movie WHERE runtimeminutes > 120)AS mov \
ON mov.movieid = movie_producer.movie'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)

# sixth query
print("\n*************************************************************************\n")
print("(Q)2.6. Alive actors who have portrayed Jesus Christ (look for both words independently)")
st = time.time()
print("Processing ...")
question1 = 'SELECT DISTINCT name \
FROM actor_movie_role \
JOIN (SELECT roleid FROM role WHERE role IN (\'["Jesus"]\',\'["Christ"]\')) AS ro \
ON ro.roleid = actor_movie_role.role \
JOIN (SELECT memberid, name FROM MEMBER WHERE deathyear IS null) AS mem \
ON mem.memberid = actor_movie_role.actor'
cursor.execute(question1)
records = cursor.fetchall()
connection.commit()
print("Result :- ", records)
print('Executed in (sec):', time.time() - st)