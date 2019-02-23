__author__ = 'BR'

"""
Author: BIKASH ROY

File name: tsvtosql34.py
"""
import psycopg2
import time
import sys


def main():
    print("Enter file names: <title>, <rating>, <crew>, <principals>, <name>")
    arguments = sys.argv
    if len(arguments) < 6:
        print("Missing arguments")
        return
    title = arguments[1]
    rating = arguments[2]
    crew = arguments[3]
    principals = arguments[4]
    name = arguments[5]

    st = time.time()

    connection = psycopg2.connect(
        host='localhost',
        dbname='sample_db',
        port='5432',
        user='',
        password=''
    )
    cursor = connection.cursor()
    connection.cursor()

    print('Dropping old database tables...')
    cursor.execute('DROP TABLE IF EXISTS movies CASCADE')
    cursor.execute('DROP TABLE IF EXISTS movieratings CASCADE')
    cursor.execute('DROP TABLE IF EXISTS names CASCADE')
    cursor.execute('DROP TABLE IF EXISTS crew CASCADE')
    cursor.execute('DROP TABLE IF EXISTS principals CASCADE')

    connection.commit()

    print('Creating database tables...')
    cursor.execute(
        '''CREATE TABLE movies
        (
            tconst text PRIMARY KEY,
            originalTitle text,
            genres text
        )'''
    )
    cursor.execute(
        '''CREATE TABLE movieratings
        (
            tconst text PRIMARY KEY,
            averageRating text,
            numVotes text 
        )'''
    )
    cursor.execute(
        '''CREATE TABLE names
        (
            nconst text,
            primaryName text,
            birthYear text,
            deathYear text ,
            primaryProfession text
        )'''
    )
    cursor.execute(
        '''CREATE TABLE crew
        (   
            tconst text PRIMARY KEY,
            writers text ,
            directors text
        )'''
    )
    cursor.execute(
        '''CREATE TABLE principals
        (
            tconst text,
            nconst text,
            category text
        )'''
    )

    with open(title) as movies:
        # movies.readline()
        for line_movies in movies:
            line_movies = line_movies.strip().split('\t')
            if line_movies[4] == "0":
                sql_movies = "INSERT INTO movies (tconst, originalTitle, genres) VALUES (%s, %s, %s)"
                val_movies = (line_movies[0], line_movies[3], line_movies[8])
                print('Inserting movies')
                cursor.execute(sql_movies, val_movies)
                connection.commit()
                with open(rating) as ratings:
                    for line_ratings in ratings:
                        line_ratings = line_ratings.strip().split('\t')
                        if line_ratings[0] == line_movies[0]:
                            sql_ratings = "INSERT INTO movieratings (tconst, averageRating, numVotes) VALUES (%s, %s, %s)"
                            val_ratings = (line_ratings[0], line_ratings[1], line_ratings[2])
                            print('Inserting ratings')
                            cursor.execute(sql_ratings, val_ratings)
                            connection.commit()
                with open(crew) as crew:
                    for line_crew in crew:
                        line_crew = line_crew.strip().split('\t')
                        if line_crew[0] == line_movies[0]:
                            sql_crew = "INSERT INTO crew (tconst, writers, directors) VALUES (%s, %s, %s)"
                            val_crew = (line_crew[0], line_crew[1], line_crew[2])
                            print('Inserting crew')
                            cursor.execute(sql_crew, val_crew)
                            connection.commit()
                with open(principals) as principals:
                    for line_principals in principals:
                        line_principals = line_principals.strip().split('\t')
                        if line_movies[0] == line_principals[0]:
                            sql_principals = "INSERT INTO principals (tconst, nconst, category) VALUES (%s, %s, %s)"
                            val_principals = (line_principals[0], line_principals[2], line_principals[3])
                            print("Inserting principals")
                            cursor.execute(sql_principals, val_principals)
                            connection.commit()
                            with open(name) as names:
                                for line_names in names:
                                    line_names = line_names.strip().split('\t')
                                    if line_principals[2] == line_names[0]:
                                        sql_names = "INSERT INTO names (nconst, primaryName, birthYear, primaryProfession) VALUES (%s, %s, %s, %s)"
                                        val_name = (line_names[0], line_names[1], line_names[2], line_names[3])
                                        print('Inserting actor')
                                        cursor.execute(sql_names, val_name)
                                        connection.commit()

    connection.close()
    print()
    print('Done.\n Executed in (sec):', time.time() - st)


if __name__ == '__main__':
    main()