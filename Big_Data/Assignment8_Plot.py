__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment8_Plot.py
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
genres = ["Action", "Horror", "Romance", "Sci-Fi", "Thriller"]
for genre in genres:
    print(genre)
    stopFlag = True
    k = range(10, 51, 5)
    plotData = {}
    for sampleSize in k:
        print(sampleSize)
        i = 0
        runSamplingLoop = True
        while i < 100:
            if runSamplingLoop is False:
                break
            sampleSizedMovies = db.movies.aggregate([
                {'$match': {'genres': {'$regex': f'{genre}', '$options': 'i'}, 'kmeansNorm': {'$exists': True}}},
                {'$sample': {'size': sampleSize}}
            ])
            centroid = db["centroids"]
            db.centroids.delete_many({})
            _id = 1
            for sample in sampleSizedMovies:
                db.centroids.insert_one({'_id': _id, 'centroid': sample['kmeansNorm']})
                _id += 1
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
                    euclideanDistances.append(
                        math.sqrt((math.pow((kmMovie['kmeansNorm'][0] - centroid['centroid'][0]), 2)
                                   + math.pow((kmMovie['kmeansNorm'][1] - centroid['centroid'][1]), 2))))
                db.movies.update_one({'_id': kmMovie['_id']},
                                     {'$set': {'cluster': (euclideanDistances.index(min(euclideanDistances)) + 1)}})
            originalCentroidList = [item["centroid"] for item in db.centroids.find()]
            runUpdateLoop = True
            while runUpdateLoop:
                for centroid in db.centroids.find():
                    if runUpdateLoop is False:
                        runSamplingLoop = False
                        break
                    clusterMovies = db.movies.find({
                        'cluster': centroid["_id"]
                    })
                    listOfStartYear = []
                    listOfAvgRating = []
                    for movie in clusterMovies:
                        listOfStartYear.append(movie['kmeansNorm'][0])
                        listOfAvgRating.append(movie['kmeansNorm'][1])
                    if len(listOfStartYear) == 0 or len(listOfAvgRating) == 0:
                        break
                    newX = sum(listOfStartYear) / len(listOfStartYear)
                    newY = sum(listOfAvgRating) / len(listOfAvgRating)
                # if centroid["centroid"][0] != newX and centroid["centroid"][1] != newY:
                    db.centroids.update_one({'_id': centroid["_id"]}, {'$set': {'centroid': [newX, newY]}})
                    i += 1

                    newCentroidList = [item["centroid"] for item in db.centroids.find()]
                    for o, n in zip(originalCentroidList, newCentroidList):
                        if n[0] - o[0] == 0 and n[1] - o[1] == 0:
                            print("In Zip")
                            runUpdateLoop = False
                            break

        SSEList = []
        for sseCentroid in db.centroids.find():
            movies = db.movies.find({'genres': genre, 'cluster': sseCentroid['_id']})
            for movie in movies:
                SSEList.append(math.pow(((sseCentroid['centroid'][0] - movie['kmeansNorm'][0])
                                         + (sseCentroid['centroid'][1] - movie['kmeansNorm'][1])), 2))
        SSE = sum(SSEList)
        plotData.update({sampleSize: SSE})
    plt.plot(*zip(*sorted(plotData.items())))
    plt.title(genre)
    plt.show()
    print("Done")