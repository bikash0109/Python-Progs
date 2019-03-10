__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment4_relationaltomongo.py
"""

from pandas import *
from collections import defaultdict
import psycopg2
import os
from pymongo import MongoClient
import pandas as pd
import json
import csv

# print("Creating imdb database in MongoDb")
# client = MongoClient()
# imdb = client["imdb"]
# db = client.test
# employee = db.employee
# df = pd.read_csv("input.csv") #csv file which you want to import
# records_ = df.to_dict(orient = 'records')
# result = db.employee.insert_many(records_ )

# host = input("Enter the db host name.")
# dbname = input("Enter db name.")
# port = input("Enter port number to connect to db")
# user = input("Enter username.")
# password = input("Enter password")
# make connection to the database
connection = psycopg2.connect(
    host="localhost",
    dbname="imdb",
    port=5432,
    user="postgres",
    password=1234
)
cursor = connection.cursor()


# def insert_records(filename, collection_name):
# #     csv_file = open(filename, 'r')
# #     reader = csv.DictReader(csv_file)
# #     db = client.imdb
# #     db.actor_movie_role.drop()
# #     header = reader.fieldnames
# #     for each in reader:
# #         row = {}
# #         for field in header:
# #             row[field] = each[field]
# #         db[collection_name].insert_one(row)
# #
# #
# # print("Migrating actor_movie_role")
# # question1 = 'select movie.movieid as _id, titletype as title, originaltitle, ' \
# #             'coalesce(startyear, 0) as startyear, coalesce(endyear, 0) as endyear, ' \
# #             'coalesce(runtimeminutes, 0) as runtime, coalesce(averagerating,0.0) as avgrating, ' \
# #             'coalesce(numvotes, 0) as numvotes, coalesce(genres,\'\') as genres ' \
# #             'from movie ' \
# #             'join movie_genre on movie_genre.movieid = movie.movieid ' \
# #             'join genre on genre.genreid = movie_genre.genreid'
# # actor_movie_role = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(question1)
# # with open('movie.csv', 'w') as f:
# #     cursor.copy_expert(actor_movie_role, f)
# # actor_movie_role_col = imdb["movie"]
# # insert_records("movie.csv", "movie")


movie = 'select movie.movieid as _id, titletype as title, originaltitle, startyear, endyear, runtimeminutes ' \
        'as runtime, ' \
        'averagerating as avgrating, numvotes, genres ' \
        'from movie ' \
        'join movie_genre on movie_genre.movieid = movie.movieid ' \
        'join genre on genre.genreid = movie_genre.genreid ' \
        'where startyear is not null ' \
        'and endyear is not null ' \
        'and runtimeminutes is not null ' \
        'and averagerating is not null ' \
        'and numvotes is not null ' \
        'and genres is not null'
cursor.execute(movie)
records = cursor.fetchall()
movieids = [item[0] for item in records]
movieidstuple = tuple(movieids)
actor = f'select actor_movie_role.actor, role.role, actor_movie_role.movie ' \
        f'from actor_movie_role ' \
        f'join role on role.roleid = actor_movie_role.role ' \
        f'where role.role is not null and actor_movie_role.movie in {movieidstuple}'
cursor.execute(actor)
actorrecords = cursor.fetchall()

finalList = []
for record in records:
    record = list(record)
    listToBeAppended = []
    for actoritem in actorrecords:
        if record[0] == actoritem[2]:
            listToBeAppended.append(actoritem[0:2])
    record.append(listToBeAppended)
    finalList.append(record)

directors = f'select movie_director.director, actor_movie_role.movie ' \
        f'from movie_director ' \
        f'where movie_director.movie in {movieidstuple}'
cursor.execute(directors)
directorsrecords = cursor.fetchall()
for record in records:
    record = list(record)
    listToBeAppended = []
    for directorItem in directorsrecords:
        if record[0] == directorItem[2]:
            listToBeAppended.append(directorItem[0:2])
    record.append(listToBeAppended)
    finalList.append(record)


movie_dict = []
headers = []
for elements in finalList:
    mydict = {"_id": elements[0],
              "type": elements[1],
              "originaltitle": elements[2],
              "startyear": elements[3],
              "endyear": elements[4],
              "runtime": elements[5],
              "avgrating": elements[6],
              "numvotes": elements[7],
              "genres": elements[8],
              "actor": elements[9]
              }
    print(mydict)
    movie_dict.append(mydict)
headers = mydict.keys()

with open('movies.csv', 'w') as f:
    w = csv.DictWriter(f, headers)
    w.writeheader()
    for row in movie_dict:
        w.writerow(row)



