__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment8.py
"""
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
from numpy import percentile
import csv
from pandas import Series
import os
import math

client = MongoClient()
db = client.IMDB_DATABASE

max_avgRating = db.movies.aggregate(
   [
     {
       '$group':
         {
           '_id': {"type": {"$type": "movie"}},
           'maxAvgRating': {'$max': "$avgRating"},
           'minAvgRating': {'$min': "$avgRating"},
           'maxStartYear': {'$max': "$startYear"},
           'minStartYear': {'$min': "$startYear"}
         }
     }
   ]
)

maxAvgRating = 0
minAvgRating = 0
maxStartYear = 0
minStartYear = 0
for record in max_avgRating:
    maxAvgRating = record['maxAvgRating']
    minAvgRating = record['minAvgRating']
    maxStartYear = record['maxStartYear']
    minStartYear = record['minStartYear']


listOfMovies = db.movies.find(
    {
        '_id': {'$exists': True},
        'type': "movie",
        'numVotes': {'$gt': 10000},
        'avgRating': {'$exists': True},
        'startYear': {'$exists': True}}
)

updateCount = 0
for movies in listOfMovies:
    normalizedStartYear = (movies['startYear'] - minStartYear)/(maxStartYear - minStartYear)
    normalizedAvgRating = (movies['avgRating'] - minAvgRating) / (maxAvgRating - minAvgRating)
    db.movies.update_one({'_id': movies['_id']}, {'$set': {'kmeansNorm': [normalizedStartYear, normalizedAvgRating]}})
    updateCount += 1

print("kmeansNorm updated count: ", updateCount)


sampleSize = input("Enter a sample size to select number of documents: ")
genre = input("Enter a genre to be match for sampling: ")

sampleSizedMovies = db.movies.aggregate([
        {'$match': {'genres': {'$regex': f'{genre}', '$options': 'i'}, 'kmeansNorm': {'$exists': True}}},
        {'$sample': {'size': int(sampleSize)}}
    ])

centroid = db["centroids"]

db.centroids.delete_many({})
_id = 1
for sample in sampleSizedMovies:
    db.centroids.insert_one({'_id': _id, 'centroid': sample['kmeansNorm']})
    _id += 1

print("Done")

listOfKmeansMovies = db.movies.find(
    {
        '_id': {'$exists': True},
        'type': "movie",
        'genres': genre,
        'numVotes': {'$gt': 10000},
        'kmeansNorm': {'$exists': True}}
)

for kmMovie in listOfKmeansMovies:
    euclideanDistances = []
    for centroid in db.centroids.find():
        euclideanDistances.append(math.sqrt((math.pow((kmMovie['kmeansNorm'][0] - centroid['centroid'][0]), 2)
                                             + math.pow((kmMovie['kmeansNorm'][1] - centroid['centroid'][1]), 2))))
    db.movies.update_one({'_id': kmMovie['_id']},
                         {'$set': {'cluster': (euclideanDistances.index(min(euclideanDistances)) + 1)}})


for centroid in db.centroids.find():
    clusterMovies = db.movies.find({
        'cluster': centroid["_id"]
    })
    listOfStartYear = []
    listOfAvgRating = []
    for movie in clusterMovies:
        listOfStartYear.append(movie['kmeansNorm'][0])
        listOfAvgRating.append(movie['kmeansNorm'][1])
    db.centroids.update_one({'_id': centroid["_id"]},
                            {'$set': {'centroid': [sum(listOfStartYear)/len(listOfStartYear),
                                                   sum(listOfAvgRating)/len(listOfAvgRating)]}})

print("Done")



