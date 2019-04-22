__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment7_itemset.py
"""
import psycopg2

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


# generalized query string, to generate the lattice
def generate_self_join_string(n, tablename):
    if n == 1:
        selfjoinsting = f"create table l{n} as \n(select"
    else:
        selfjoinsting = f"create table l{n} as \n(select "
        for i in range(1, n):
            selfjoinsting += f"l{n-1}.actor{i}, "
        selfjoinsting += f"popmovact.actor{n}, popmovact.count \nfrom \nl{n-1}, \n(select"
    for i in range(1, n+1):
        selfjoinsting += f" tbl{i}.actor as actor{i}, "
    selfjoinsting += " count(tbl1.movie) as count \nfrom "
    for i in range(1, n+1):
        selfjoinsting += tablename + f" tbl{i}, "
    selfjoinsting = selfjoinsting.rstrip(", ") + (" \nwhere \n" if n > 1 else "")
    for i in range(1, n):
        selfjoinsting += f"tbl{i}.movie = tbl{i+1}.movie and \n"
    for i in range(1, n):
        selfjoinsting += f"tbl{i}.actor < tbl{i+1}.actor and \n"
    selfjoinsting = selfjoinsting.rstrip("and \n") + " \ngroup by "
    for i in range(1, n+1):
        selfjoinsting += f"tbl{i}.actor, "
    if n == 1:
        selfjoinsting = selfjoinsting.rstrip(", ") + " \nhaving count(tbl1.movie) >= 5"
    else:
        selfjoinsting = selfjoinsting.rstrip(", ") + " \nhaving count(tbl1.movie) >= 5) as popmovact \nwhere "
        for i in range(1, n):
            selfjoinsting += f"popmovact.actor{i} = l{n-1}.actor{i} and "
    selfjoinsting = selfjoinsting.rstrip("and ") + ")"
    return selfjoinsting


# this portion of the code, creates the tables, unless an empty table is created
stop = True
count = 1
while stop:
    selfjointable = generate_self_join_string(count, "Popular_Movie_Actors")
    cursor.execute(f'DROP TABLE IF EXISTS l{count} CASCADE')
    cursor.execute(selfjointable)
    connection.commit()
    cursor.execute(f'select count(*) from l{count}')
    records = cursor.fetchall()
    print(f"number of frequent itemsets in level {count} = ", records[0][0])
    count += 1
    if records[0][0] == 0:
        stop = False


# This portion of code, deals with the last past of the assignment, where all the actor names are to be displayed

# get all actor lists of l6
cursor.execute(f'select * from l6')
records = cursor.fetchall()
allmemberid = []
for row in records:
    allmemberid.extend(list(row)[:-1])
alluniqueid = set(allmemberid)  # get only the unique ids

# get all the names from the member table
q = f'select member.memberid , name from member where memberid in {(alluniqueid)}'
q = q.replace("{", "(").replace("}", ")")
cursor.execute(q)
memberRecords = cursor.fetchall()

# replace the actor id with their real name
print()
for row in records:
    output = str(row)
    for item in memberRecords:
        if item[0] in row:
            output = output.replace(str(item[0]), item[1])
    print(output)
    print()

