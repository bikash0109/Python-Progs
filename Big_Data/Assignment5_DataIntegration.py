__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment5_DataIntegration.py
"""
# a python program to load the views and materialized views.
import psycopg2
import time

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
# a db connection variable
cursor = connection.cursor()

# deleting any old tables existing of same name
print('Dropping old views...')
cursor.execute('DROP VIEW IF EXISTS ComedyMovie CASCADE')
cursor.execute('DROP VIEW IF EXISTS NonComedyMovie CASCADE')
cursor.execute('DROP VIEW IF EXISTS ComedyActor CASCADE')
cursor.execute('DROP VIEW IF EXISTS NonComedyActor CASCADE')
cursor.execute('DROP VIEW IF EXISTS ActedIn CASCADE')
cursor.execute('DROP MATERIALIZED VIEW IF EXISTS MaterializedComedyMovie CASCADE')
cursor.execute('DROP MATERIALIZED VIEW IF EXISTS MaterializedNonComedyMovie CASCADE')
cursor.execute('DROP MATERIALIZED VIEW IF EXISTS MaterializedComedyActor CASCADE')
cursor.execute('DROP MATERIALIZED VIEW IF EXISTS MaterializedNonComedyActor CASCADE')
cursor.execute('DROP MATERIALIZED VIEW IF EXISTS MaterializedActedIn CASCADE')
cursor.execute('DROP VIEW IF EXISTS All_Movie CASCADE')
cursor.execute('DROP VIEW IF EXISTS All_Actor CASCADE')
cursor.execute('DROP VIEW IF EXISTS All_Movie_Actor CASCADE')
connection.commit()

print("1. Creating views and materialized view")
print("\tCreating ComedyMovie")
cursor.execute('create view ComedyMovie as select movie.movieid as id, primarytitle as title, startyear as year '
               'from movie '
               'join movie_genre on movie_genre.movieid = movie.movieid '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres ilike \'%Comedy%\' and runtimeminutes >= 75')

print("\tCreating MaterializedComedyMovie")
cursor.execute('create materialized view MaterializedComedyMovie as select movie.movieid as id, primarytitle as title, '
               'startyear as year '
               'from movie '
               'join movie_genre on movie_genre.movieid = movie.movieid '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres ilike \'%Comedy%\' and runtimeminutes >= 75')

print("\tCreating NonComedyMovie")
cursor.execute('create view NonComedyMovie as select movie.movieid as id, primarytitle as title, startyear as year '
               'from movie '
               'join movie_genre on movie_genre.movieid = movie.movieid '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres not ilike \'%Comedy%\' and runtimeminutes >= 75')

print("\tCreating MaterializedNonComedyMovie")
cursor.execute('create materialized view MaterializedNonComedyMovie as select movie.movieid as id, primarytitle '
               'as title, startyear as year '
               'from movie '
               'join movie_genre on movie_genre.movieid = movie.movieid '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres not ilike \'%Comedy%\' and runtimeminutes >= 75')

print("\tCreating ComedyActor")
cursor.execute('create view ComedyActor as select member.memberid as id, name, birthyear, deathyear '
               'from member '
               'join movie_actor on movie_actor.actor = member.memberid '
               'join movie_genre on movie_genre.movieid = movie_actor.movie '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres ilike \'%Comedy%\'')

print("\tCreating MaterializedComedyActor")
cursor.execute('create materialized view MaterializedComedyActor as select member.memberid as id, name, birthyear, '
               'deathyear '
               'from member '
               'join movie_actor on movie_actor.actor = member.memberid '
               'join movie_genre on movie_genre.movieid = movie_actor.movie '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres ilike \'%Comedy%\'')

print("\tCreating NonComedyActor")
cursor.execute('create view NonComedyActor as select member.memberid as id, name, birthyear, deathyear '
               'from member '
               'join movie_actor on movie_actor.actor = member.memberid '
               'join movie_genre on movie_genre.movieid = movie_actor.movie '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres not ilike \'%Comedy%\'')

print("\tCreating MaterializedNonComedyActor")
cursor.execute('create materialized view MaterializedNonComedyActor as select member.memberid as id, name, birthyear, '
               'deathyear '
               'from member '
               'join movie_actor on movie_actor.actor = member.memberid '
               'join movie_genre on movie_genre.movieid = movie_actor.movie '
               'join genre on genre.genreid = movie_genre.genreid '
               'where genres not ilike \'%Comedy%\'')

print("\tCreating ActedIn")
cursor.execute('create view ActedIn as select * from movie_actor')

print("\tCreating MaterializedActedIn")
cursor.execute('create materialized view MaterializedActedIn as select * from movie_actor')
connection.commit()
print("\n***********************************************************************************************************\n")

print("2. Creating GAV views")
print("\tCreating All_Movie")
cursor.execute('create view All_Movie as select *, \'Comedy\' as genre from comedymovie union select *, \'NonComedy\' '
               'as genre from noncomedymovie')

print("\tCreating All_Actor")
cursor.execute('create view All_Actor as select * from comedyactor union select * from noncomedyactor')

print("\tCreating All_Movie_Actor")
cursor.execute('create view All_Movie_Actor as select * from actedin')
connection.commit()
print("\n***********************************************************************************************************\n")

print("3. Q1")
print("select name \n\
from all_actor \n\
join all_movie_actor on all_movie_actor.actor = all_actor.id \n\
join all_movie on all_movie.id = all_movie_actor.movie \n\
where year > 2000 and year < 2005 and deathyear is null \n\
group by name \n\
having count(all_actor.id) > 10")

print("3. Q2")
print("select distinct name \n\
from all_actor \n\
join all_movie_actor on all_movie_actor.actor = all_actor.id \n\
join all_movie on all_movie.id = all_movie_actor.movie \n\
where name ilike 'Ja%' and genre != 'Comedy'")
print("\n***********************************************************************************************************\n")

# start logging time
st = time.time()
print("4. Calculating time for view")
cursor.execute('select name '
               'from (select * from comedyactor union select * from noncomedyactor) as all_actor '
               'join (select * from actedin) as all_movie_actor on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from comedymovie union select *, \'NonComedy\' as genre '
               'from noncomedymovie) as all_movie on all_movie.id = all_movie_actor.movie '
               'where year > 2000 and year < 2005 and deathyear is null '
               'group by name '
               'having count(all_actor.id) > 10')

cursor.execute('select distinct name '
               'from (select * from comedyactor union select * from noncomedyactor) as all_actor '
               'join (select * from actedin) as all_movie_actor on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from comedymovie union select *, \'NonComedy\' as genre '
               'from noncomedymovie) as all_movie on all_movie.id = all_movie_actor.movie where name ilike \'Ja%\' '
               'and genre != \'Comedy\'')
print('Done.\n Executed view in (sec):', time.time() - st)

st = time.time()
print("4. Calculating time for materialized view")
cursor.execute('select name '
               'from (select * from materializedcomedyactor union select * from materializednoncomedyactor) '
               'as all_actor '
               'join (select * from materializedactedin) as all_movie_actor on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from materializedcomedymovie union select *, \'NonComedy\' '
               'as genre '
               'from materializednoncomedymovie) as all_movie on all_movie.id = all_movie_actor.movie '
               'where year > 2000 and year < 2005 and deathyear is null '
               'group by name '
               'having count(all_actor.id) > 10')

cursor.execute('select distinct name '
               'from (select * from materializedcomedyactor union select * from materializednoncomedyactor) '
               'as all_actor '
               'join (select * from materializedactedin) as all_movie_actor on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from materializedcomedymovie union select *, \'NonComedy\' '
               'as genre '
               'from materializednoncomedymovie) as all_movie on all_movie.id = all_movie_actor.movie '
               'where name ilike \'Ja%\' '
               'and genre != \'Comedy\'')
print('Done.\n Executed materialized view in (sec):', time.time() - st)
print("\n***********************************************************************************************************\n")

st = time.time()
print("5. Calculating time for view 3.1 query optimization")
cursor.execute('select name '
               'from (select * from comedyactor where deathyear is null '
               'union '
               'select * from noncomedyactor where deathyear is null) '
               'as all_actor '
               'join (select * from actedin) as all_movie_actor '
               'on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from comedymovie '
               'where year > 2000 and year < 2005 '
               'union '
               'select *, \'NonComedy\' as genre from noncomedymovie '
               'where year > 2000 and year < 2005) as all_movie '
               'on all_movie.id = all_movie_actor.movie '
               'group by name '
               'having count(all_actor.id) > 10')
print('Done.\n Executed with view in (sec):', time.time() - st)
print("\n***********************************************************************************************************\n")

st = time.time()
print("5. Calculating time for materialized view 3.1 query optimization")
cursor.execute('select name '
               'from (select * from materializedcomedyactor where deathyear is null '
               'union '
               'select * from materializednoncomedyactor where deathyear is null) '
               'as all_actor '
               'join (select * from materializedactedin) as all_movie_actor '
               'on all_movie_actor.actor = all_actor.id '
               'join (select *, \'Comedy\' as genre from materializedcomedymovie '
               'where year > 2000 and year < 2005 '
               'union '
               'select *, \'NonComedy\' as genre from materializednoncomedymovie '
               'where year > 2000 and year < 2005) as all_movie '
               'on all_movie.id = all_movie_actor.movie '
               'group by name '
               'having count(all_actor.id) > 10')
print('Done.\n Executed with view in (sec):', time.time() - st)
print("\n***********************************************************************************************************\n")


st = time.time()
print("5. Calculating time for view 3.2 query optimization")
cursor.execute('select distinct name '
               'from noncomedyactor '
               'join actedin on actedin.actor = noncomedyactor.id '
               'join noncomedymovie on noncomedymovie.id = actedin.movie '
               'where name ilike \'Ja%\'')
print('Done.\n Executed with view in (sec):', time.time() - st)
print("\n***********************************************************************************************************\n")

st = time.time()
print("5. Calculating time for materialized view 3.2 query optimization")
cursor.execute('select distinct name '
               'from materializednoncomedyactor '
               'join materializedactedin on materializedactedin.actor = materializednoncomedyactor.id '
               'join materializednoncomedymovie on materializednoncomedymovie.id = materializedactedin.movie '
               'where name ilike \'Ja%\'')
print('Done.\n Executed with view in (sec):', time.time() - st)
print("\n***********************************************************************************************************\n")