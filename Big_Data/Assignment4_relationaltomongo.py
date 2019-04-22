__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment4_relationaltomongo.py
Program to migrate data from Postgres to MongoDb
"""
import psycopg2
import os
from pymongo import MongoClient
import csv
import time
import gc

print("Creating imdb database in MongoDb")
client = MongoClient()
imdb = client["imdb_db"]
moviecol = imdb["movies"]
membercol = imdb["members"]

print("Enter details for Postgres Connection")
# host = input("Enter the db host name.")
# dbname = input("Enter db name.")
# port = input("Enter port number to connect to db")
# user = input("Enter username.")
# password = input("Enter password")
# make connection to the database
connection = psycopg2.connect(
    host='localhost',
    dbname='imdb',
    port=5432,
    user='postgres',
    password=1234
)
cursor = connection.cursor()


def insert_records(filename, collection_name):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)
    db = client.imdb_db
    db.collection_name.drop()
    header = reader.fieldnames
    for each in reader:
        line = {}
        for field in header:
            line[field] = each[field]
        db[collection_name].insert_one(line)


st = time.time()
print("Migrating movies")
movie = 'select distinct on (movie.movieid) movie.movieid as _id, titletype as title, originaltitle, ' \
        'coalesce(startyear, 0) as startyear, ' \
        'coalesce(endyear, 0) as endyear, coalesce(runtimeminutes, 0) as runtime, ' \
        'coalesce(averagerating, 0.0) as avgrating, coalesce(numvotes, 0.0) as numvotes, ' \
        'coalesce(genres, \'\') as genres ' \
        'from movie ' \
        'join movie_genre on movie_genre.movieid = movie.movieid ' \
        'join genre on genre.genreid = movie_genre.genreid '
movies_query = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(movie)
with open('movies.csv', 'w') as f:
    cursor.copy_expert(movies_query, f)

# cursor.execute(movie)
movieids = []
records = []
with open('movies.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    for row in csv_reader:
        if counter > 0:
            record = row
            actor = f'select actor_movie_role.actor, actor_movie_role.role, actor_movie_role.movie ' \
                    f'from actor_movie_role where actor_movie_role.movie = {row[0]} '
            cursor.execute(actor)
            actorrecords = cursor.fetchall()
            rolerecords = []
            if len(actorrecords) > 0:
                role = f'select role.role ' \
                       f'from role where role.roleid = {actorrecords[0][1]} '
                cursor.execute(role)
                rolerecords = cursor.fetchall()

            print("Inserting Actors- Roles")
            listActDict = []
            actDict = {"actor": actorrecords[0] if len(actorrecords) > 0 else [],
                       "roles": rolerecords[0] if len(rolerecords) > 0 else []}
            record.append(listActDict.append(actDict))

            print("Inserting Directors")
            directors = f'select movie_director.director, movie_director.movie ' \
                        f'from movie_director ' \
                        f'where movie_director.movie = {row[0]}'
            cursor.execute(directors)
            directorsrecords = cursor.fetchall()
            dirDict = tuple(directorsrecords[0] if len(directorsrecords) > 0 else [])
            record.append(dirDict)

            print("Inserting Writers")
            writers = f'select movie_writer.writer, movie_writer.movie ' \
                      f'from movie_writer ' \
                      f'where movie_writer.movie = {row[0]}'
            cursor.execute(writers)
            writersrecords = cursor.fetchall()
            wirDict = tuple(writersrecords[0] if len(writersrecords) > 0 else [])
            record.append(wirDict)

            print("Inserting producers")
            producers = f'select movie_producer.producer, movie_producer.movie ' \
                        f'from movie_producer ' \
                        f'where movie_producer.movie = {row[0]}'
            cursor.execute(writers)
            producersrecords = cursor.fetchall()
            prodDict = tuple(producersrecords[0] if len(producersrecords) > 0 else [])
            record.append(prodDict)
            mydict = {"_id": record[0],
                      "type": record[1],
                      "originaltitle": record[2],
                      "startyear": record[3],
                      "endyear": record[4],
                      "runtime": record[5],
                      "avgrating": record[6],
                      "numvotes": record[7],
                      "genres": record[8],
                      "actor": record[9],
                      "directors": record[10],
                      "writers": record[11],
                      "producers": record[12]
                      }
            moviecol.insert_one(mydict)
        if counter == 0:
            counter += 1


print("Migrating members")
question1 = 'select memberid as _id, name, birthyear, deathyear ' \
            'from member ' \
            'where birthyear is not null ' \
            'and deathyear is not null'
members_query = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(question1)
with open('members.csv', 'w') as f:
    cursor.copy_expert(members_query, f)
print("Commit members collection")
insert_records("members.csv", "members")

print("Deleting temp files")
os.remove("movies.csv")
os.remove("members.csv")
print('Done.\n Executed in (sec):', time.time() - st)