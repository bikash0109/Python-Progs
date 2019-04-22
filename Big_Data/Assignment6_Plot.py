__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment6_Plot.py
"""
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
from numpy import percentile
import csv
from pandas import Series
import os

client = MongoClient()
db = client.IMDB_DATABASE

totalGenres = db.movies.aggregate([
    {'$project': {'_id': 0, 'genres': 1}},
    {'$unwind': "$genres"},
    {'$group': {'_id': "$genres", 'count': {'$sum': 1}}}
])

listOfAllGenres = [record['_id'] for record in totalGenres]

anotherWay = db.movies.aggregate([
    {'$project': {'_id': 0, 'numVotes': 1, 'genres': 1, 'avgRating': 1}},
    {'$unwind': "$genres"},
    {'$match': {'numVotes': {'$gt': 10000}}}
])

listOfLists = {}
for genre in listOfAllGenres:
    listOfLists['list_%s' %genre] = []

for item in anotherWay:
    if item["genres"] in listOfAllGenres:
        listname = f'list_{item["genres"]}'
        listOfLists[listname].append(item["avgRating"])


print("Q4.1. For each genre, a five-number summary of the average ratings of movies with more than 10K votes")
for k in listOfLists:
    if len(listOfLists[k]) == 0:
        continue
    data = listOfLists[k]
    # calculate quartiles
    quartiles = percentile(data, [25, 50, 75])
    # calculate min/max
    data_min, data_max = min(data), max(data)
    # print 5-number summary
    print(str(k[5:]))
    print('Min: %.3f' % data_min)
    print('Q1: %.3f' % quartiles[0])
    print('Median: %.3f' % quartiles[1])
    print('Q3: %.3f' % quartiles[2])
    print('Max: %.3f' % data_max)
    print()
    objects = ('Min', 'Q1', 'Median', 'Q3', 'Max')
    y_pos = np.arange(len(objects))
    performance = [data_min, quartiles[0], quartiles[1], quartiles[2], data_max]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(str(k[5:] + "- avgRating"))
    plt.title('five number summary')
    plt.show()

anotherWayActors = db.movies.aggregate([
    {'$project': {'_id': 0, 'genres': 1, 'actors.actor': 1}},
    {'$unwind': "$genres"},
    {'$match': {'actors': {"$ne": None}}}
])

listOfListsActors = {}
for genre in listOfAllGenres:
    listOfListsActors['actor_list_%s' %genre] = []
for actors in anotherWayActors:
    if actors["genres"] in listOfAllGenres:
        listname = f'actor_list_{actors["genres"]}'
        listOfListsActors[listname].append(len(actors["actors"]))

print("Q4.2 Average number of actors in movies by genre as a bar chart for all movies with any actors "
      "(i.e. skip documents with no “actors” field).")
for k in listOfListsActors:
    if len(listOfListsActors[k]) == 0:
        continue
    data = listOfListsActors[k]
    # calculate min/max
    data_avg = sum(data)/len(data)
    data_min, data_max = min(data), max(data)
    # Average number of actors
    print(str(k[11:]))
    print('Avg: %.3f' % data_avg)
    print()
    objects = ('Min', 'Avg', 'Max')
    y_pos = np.arange(len(objects))
    performance = [data_min, data_avg, data_max]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(str(k[11:] + "- number of movies"))
    plt.title('Average number of actors')
    plt.show()


print("Q4.3 Number of movies produced each year (startYear) as a time series plot.")
anotherWayStartYear = db.movies.aggregate([
    {'$group': {"_id": "$startYear", "startYears": {'$addToSet': "$_id"}}},
    {'$project': {"startYear": "$_id", "_id": 0, "Num_Movies": {'$size': '$startYears'}}},
    {'$match': {'startYear': {"$ne": None}}}
])

with open('anotherWayStartYear.csv', 'w') as outfile:
    fields = ['startYear', 'Num_Movies']
    write = csv.DictWriter(outfile, fieldnames=fields)
    write.writeheader()
    for answers_record in anotherWayStartYear:  # Here we are using 'cursor' as an iterator
        if len(answers_record) != 2:
            continue
        flattened_record = {
            'startYear': answers_record["startYear"],
            'Num_Movies': answers_record["Num_Movies"]
        }
        write.writerow(flattened_record)


series = Series.from_csv('anotherWayStartYear.csv', header=0)
series.plot()
plt.show()
os.remove("anotherWayStartYear.csv")
