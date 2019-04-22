import psycopg2
import pymongo
import math

"""
Create a connection code with the postresql sql
"""
connection = psycopg2.connect(user = "postgres",
                                  password = "12345",
                                  host = "127.0.0.1",
                                  port = "5433",
                                  database = "postgres")

cursor = connection.cursor()


myclient = pymongo.MongoClient("127.0.0.1")  # connection to mongo db created
mydb = myclient["IMDB"] # IMDB mongo db created


MemberMongo = mydb["Member"] # connection to Member collection
MovieMongo = mydb["Movie"] # connection to Movie collection
CentroidsMongo = mydb["Centroids"] # connetion to Extra data collection


def main():

    doc = MovieMongo.aggregate([
            {
              '$group': {
                        '_id': "$type",
                        'minStartYear': {'$min': '$startYear'},
                        'minQuantity': {'$min': '$avgRating'},
                        'maxStartYear': {'$max': "$startYear"},
                        'maxQuantity': {'$max': "$avgRating"}}}])

    dictlist = []
    for val in doc:
        for key, value in val.items():
            temp = [key, value]
            dictlist.append(temp)

    maxstartyear = []
    maxavgRating = []
    minstartyear = []
    minavgRating = []

    for list in dictlist:
        if 'maxStartYear' in list:
            maxstartyear.append(list[1])
        elif 'maxQuantity' in list:
            maxavgRating.append(list[1])
        elif 'minStartYear' in list:
            minstartyear.append(list[1])
        elif 'minQuantity' in list:
            minavgRating.append(list[1])

    maxStartYear = max(maxstartyear)
    maxAvgRating = max(maxavgRating)
    minStartYear = min(minstartyear)
    minAvgRating = min(minavgRating)

    print("The maximum startyear is: ", maxStartYear)
    print("The minimum startyear is: ", minStartYear)
    print("The maximum average rating is: ", maxAvgRating)
    print("The minimum average rating is: ", minAvgRating)

    """
    x=MovieMongo.aggregate([
        {'$match': {'startYear': {'$exists': True}, 'avgRating': {'$exists': True}, 'type': 'movie', 'numVotes': {'$gt':10000}}},
        {'$addFields': {'KmeansNorm': [{'$divide': [{'$subtract': ["$startYear", minStartYear]}, {'$subtract': [maxStartYear, minStartYear]}]},
                                       {'$divide': [{'$subtract': ["$avgRating", minAvgRating]},
                                                    {'$subtract': [maxAvgRating, minAvgRating]}]}]}}
    ])
    """

    x = MovieMongo.find({'type': 'movie', 'numVotes': {'$gt': 10000}, 'avgRating': {'$exists': True}, 'startYear': {'$exists': True}})
    for docs in x:
        if docs['_id'] is not None:
            id = docs['_id']
            sy = docs['startYear']
            numerator1 = sy - minStartYear
            denominator1 = maxStartYear - minStartYear
            result1 = numerator1/denominator1
            avgr = docs['avgRating']
            numerator2 = avgr - minAvgRating
            denominator2 = maxAvgRating - minAvgRating
            result2 = numerator2/denominator2
            MovieMongo.update_one({'_id': id }, {'$set': {'KmeansNorm': [result1, result2]}})

    num = input("enter a random number")
    genre = input("enter a valid genre")
    k = int(num)



    val = MovieMongo.aggregate([
        {'$match': {'genres': genre, 'KmeansNorm': {'$exists': True}}},
        {'$sample': {'size': k}}
    ])

    CentroidsMongo.delete_many({})

    d = 0
    for v in val:
        d = d+1
        CentroidsMongo.insert_one({'_id': d, 'Knorm': v['KmeansNorm']})

    z = CentroidsMongo.find()
    for val in z:
        print(val)


    print()
    print()

    genre_movie = MovieMongo.find({'genres': genre, 'type': 'movie', 'numVotes': {'$gt': 10000}, 'KmeansNorm': {'$exists': True}})

    edlist = []
    for movies in genre_movie:
        movid = movies['_id']
        t = 0
        p = CentroidsMongo.find()
        for rm in p:
            t = t + 1
            EUdist = math.sqrt((math.pow((movies['KmeansNorm'][0] - rm['Knorm'][0]), 2) + math.pow((movies['KmeansNorm'][1] - rm['Knorm'][1]), 2)))
            edlist.append(EUdist)

        minid =(edlist.index(min(edlist))) + 1

        # total_Movie_Updates = MovieMongo.find({'movie': genre, 'type': 'movie', 'numVotes': {'$gt': 10000}})

        # for mov in total_Movie_Updates:
        MovieMongo.update_one({'_id': movid}, {'$set': {'Cluster': [minid]}})

        edlist = []

    total = MovieMongo.find({'Cluster': {'$exists': True}})


    # for t in total:
    #     print(t)


    p = CentroidsMongo.find()

    xcordlist = []
    ycordlist = []
    for c in p:
        ID = c['_id']
        x = MovieMongo.find({'Cluster': [ID]})
        for mov in x:
            xval = mov['KmeansNorm'][0]
            yval = mov['KmeansNorm'][1]
            xcordlist.append(xval)
            ycordlist.append(yval)
        if len(xcordlist) != 0 and len(ycordlist) != 0:
            UpdatedX = sum(xcordlist)/len(xcordlist)
            UpdatedY = sum(ycordlist)/len(ycordlist)
            CentroidsMongo.update_one({'_id': ID}, {'$set': {'Knorm': [UpdatedX, UpdatedY]}})
        xcordlist = []
        ycordlist = []

    finalCentroid = CentroidsMongo.find()
    for c in finalCentroid:
        print(c)

    print("-----------------------------------------------------------------------------------------------------------")
    print("Task 4:")


    
    movie_genre = MovieMongo.distinct('genres')
    for mg in movie_genre:
        print(mg)
    

    k = 10
    while k <= 50:
        movie_genre = MovieMongo.distinct('genres')
        for mg in movie_genre:
            if 'Action' in mg or 'Horror' in mg or 'Romance' in mg or 'Sci-Fi' in mg or 'Thriller' in mg:
                while 1:
                    l = 0
                    val2 = MovieMongo.aggregate([
                        {'$match': {'genres': mg, 'KmeansNorm': {'$exists': True}}},
                        {'$sample': {'size': k}}
                    ])

                    CentroidsMongo.delete_many({})

                    d2 = 0
                    for v in val2:
                        d2 = d2 + 1
                        CentroidsMongo.insert_one({'_id': d2, 'Knorm': v['KmeansNorm']})

                    c = CentroidsMongo.find()

                    originalCentroidList = []

                    for cen in c:
                        originalCentroidList.append(cen['Knorm'])

                    genre_movie2 = MovieMongo.find({'genres': mg, 'type': 'movie', 'numVotes': {'$gt': 10000}, 'KmeansNorm': {'$exists': True}})

                    edlist2 = []
                    for movies2 in genre_movie2:
                        movid2 = movies2['_id']
                        t2 = 0
                        p2 = CentroidsMongo.find()
                        for rm2 in p2:
                            t2 = t2 + 1
                            EUdist2 = math.sqrt((math.pow((movies2['KmeansNorm'][0] - rm2['Knorm'][0]), 2) + math.pow((movies2['KmeansNorm'][1] - rm2['Knorm'][1]), 2)))
                            edlist2.append(EUdist2)

                        minid2 = (edlist2.index(min(edlist2))) + 1
                        MovieMongo.update_one({'_id': movid2}, {'$set': {'Cluster': [minid2]}})
                        edlist2 = []

                    p2 = CentroidsMongo.find()

                    xcordlist2 = []
                    ycordlist2 = []
                    for c in p2:
                        ID = c['_id']
                        x = MovieMongo.find({'Cluster': [ID]})
                        for mov in x:
                            xval = mov['KmeansNorm'][0]
                            yval = mov['KmeansNorm'][1]
                            xcordlist2.append(xval)
                            ycordlist2.append(yval)
                        if len(xcordlist) != 0 and len(ycordlist) != 0:
                            UpdatedX = sum(xcordlist2) / len(xcordlist2)
                            UpdatedY = sum(ycordlist2) / len(ycordlist2)
                            CentroidsMongo.update_one({'_id': ID}, {'$set': {'Knorm': [UpdatedX, UpdatedY]}})
                        xcordlist2 = []
                        ycordlist2 = []

                    e = CentroidsMongo.find()
                    newCentroidList = []
                    for nc in e:
                        newCentroidList.append(nc['Knorm'])

                    for o, n in zip(originalCentroidList, newCentroidList):
                        if n[0] - o[0] == 0 and n[1] - o[1] == 0:
                            l = 1

                    if l == 1:
                        sumofsquarederrorlist = []
                        centroids = CentroidsMongo.find()
                        for cen in centroids:
                            fm = MovieMongo.find({'genres': mg, 'Cluster': cen['_id']})
                            for mov in fm:
                                sse = math.pow((cen['Knorm'][0] - mov['KmeansNorm'][0]) + (cen['Knorm'][1] - mov['KmeansNorm'][1]), 2)
                                sumofsquarederrorlist.append(sse)
                        totalerror = sum(sumofsquarederrorlist)
                        break
            else:
                print("\n")
                continue
        k = k + 5






if __name__=="__main__":
    main()