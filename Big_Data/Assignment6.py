__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment6_Plot.py
"""
from pymongo import MongoClient
import matplotlib.pyplot as plt; plt.rcdefaults()

client = MongoClient()
db = client.IMDB_DATABASE

updateCount = 0
extra_data = db["extra-data"].find()
for data in extra_data:
    if 'IMDb_ID' in data and 'box_office_currencyLabel' in data:
        if data['box_office_currencyLabel']['value'] == 'United States dollar':
            revenue = data['box_office']['value'] if 'box_office' in data else 0
            cost = data['cost']['value'] if 'cost' in data else 0
            distributor = data['distributorLabel']['value'] if 'distributorLabel' in data else ''
            rating = data['MPAA_film_ratingLabel']['value'] if 'MPAA_film_ratingLabel' in data else ''
            _id = int(data['IMDb_ID']['value'][2:])
            recordUpdated = db.movies.update_one({'_id': _id}, {'$set': {'revenue': revenue, 'cost': cost,
                                                                         'distributor': distributor,
                                                                         'rating': rating}})
            updateCount += 1


print("Total records updated = ", updateCount)


duplicates = db["extra-data"].aggregate([
    {"$match": {"IMDb_ID.value": {"$ne": 'null'}}},
    {"$group": {"_id": "$IMDb_ID.value", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}},
    {"$project": {"duplicate_id": "$_id", "_id": 0}}
])

dupCount = 0
for item in duplicates:
    dupCount += 1
print("Duplicate count", dupCount)

matchDpCount = 0
extra_data_again = db["extra-data"].find()
for data in extra_data_again:
    if 'IMDb_ID' in data and 'box_office_currencyLabel' in data:
        if data['box_office_currencyLabel']['value'] == 'United States dollar':
            title = data['titleLabel']['value']
            matchedRecords = db.movies.find({'title': title})
            print("For movie title \"" + title + "\" there are total of \""
                  + str(matchedRecords.count()) + "\" matching records")
            if matchedRecords.count() > 1:
                matchDpCount += matchedRecords.count()
print("Total duplicate values : ", matchDpCount)
