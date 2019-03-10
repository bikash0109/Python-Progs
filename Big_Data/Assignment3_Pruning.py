__author__ = 'BR'

"""
Author: BIKASH ROY

File name: Assignment3_Prunning.py
Algorithm to find FD is taken from this paper below:
https://www.lri.fr/~pierres/donn%E9es/save/these/articles/lpr-queue/huhtala99tane.pdf

Since naive takes a lot of time, this algorithm TANE is much faster, hence using it.
"""

from pandas import *
from collections import defaultdict
import psycopg2
import os


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
cursor = connection.cursor()


# Get FD's from the table, Algorithm as per the paper below -
# https://www.lri.fr/~pierres/donn%E9es/save/these/articles/lpr-queue/huhtala99tane.pdf
def get_functional_dependency(partition):
    global tuple_mapping
    global listofcolumns
    for row in partition:
        subsetOfFunctionalDependencies = []
        for attribute in row:
            if row.replace(attribute, '') in tuple_mapping.keys():
                temp = tuple_mapping[row.replace(attribute, '')]
            else:
                temp = listofcolumns
                tuple_mapping[row.replace(attribute, '')] = temp
            subsetOfFunctionalDependencies.insert(0, set(temp))
        if list(set.intersection(*subsetOfFunctionalDependencies)) is []:
            tuple_mapping[row] = []
        else:
            tuple_mapping[row] = list(set.intersection(*subsetOfFunctionalDependencies))
    for row in partition:
        for attribute in row:
            if attribute in tuple_mapping[row]:
                if validfd(row.replace(attribute, ''), attribute):
                    functional_dependencies.append([row.replace(attribute, ''), attribute])
                    tuple_mapping[row].remove(attribute)
                    listofcols = listofcolumns[:]
                    for j in row:
                        if j in listofcols: listofcols.remove(j)
                    for b in listofcols:
                        if b in tuple_mapping[row]: tuple_mapping[row].remove(b)


# Check if a FD is valid or not
def validfd(y, z):
    if y == '' or z == '':
        return False
    ey = computeE(y)
    eyz = computeE(y + z)
    if ey == eyz:
        return True
    else:
        return False


# Compute algorithm - https://www.lri.fr/~pierres/donn%E9es/save/these/articles/lpr-queue/huhtala99tane.pdf
def computeE(x):
    global totaltuples
    global partition_list
    doublenorm = 0
    for i in partition_list[''.join(sorted(x))]:
        doublenorm = doublenorm + len(i)
    e = (doublenorm - len(partition_list[''.join(sorted(x))])) / float(totaltuples)
    return e


# Get the next set of partition to work upon
def get_next_partition(level):
    partition = []
    for i in range(0, len(level)):
        for j in range(i + 1, len(level)):
            if (not level[i] == level[j]) and level[i][0:-1] == level[j][0:-1]:
                x = level[i] + level[j][-1]
                flag = True
                for a in x:
                    if not (x.replace(a, '') in level):
                        flag = False
                if flag:
                    partition.append(x)
                    stripped_partitions(x, level[i], level[j])
    return partition


# Stripped partition algorithm, as per - 
# https://www.lri.fr/~pierres/donn%E9es/save/these/articles/lpr-queue/huhtala99tane.pdf
def stripped_partitions(x, y, z):
    global partition_list
    global table_tuple
    table_stripped = [''] * len(table_tuple)
    partition_first = partition_list[''.join(sorted(y))] # partition_first is a list of lists, each list is an equivalence class
    partition_last = partition_list[''.join(sorted(z))] # partition_last is a list of lists, each list is an equivalence class
    partition_data = []
    for i in range(len(partition_first)):
        for t in partition_first[i]:
            table_tuple[t] = i
        table_stripped[i] = ''
    for i in range(len(partition_last)):
        for t in partition_last[i]:
            if not (table_tuple[t] == 'NULL'):
                table_stripped[table_tuple[t]] = sorted(list(set(table_stripped[table_tuple[t]]) | set([t])))
        for t in partition_last[i]:
            if (not (table_tuple[t] == 'NULL')) and len(table_stripped[table_tuple[t]]) >= 2:
                partition_data.append(table_stripped[table_tuple[t]])
            if not (table_tuple[t] == 'NULL'): table_stripped[table_tuple[t]] = ''
    for i in range(len(partition_first)):
        for t in partition_first[i]:
            table_tuple[t] = 'NULL'
    partition_list[''.join(sorted(x))] = partition_data


# getting the equivalent classes of the attributes
def equivalence_class(seq):
    classes = defaultdict(list)
    for i, item in enumerate(seq):
        classes[item].append(i)
    return ((key, val) for key, val in classes.items() if len(val) > 0)


# Creating a dummy file from the DB, to process execution faster. File will be deleted at the end
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format('SELECT * FROM movie_all')
with open('resultsfile.csv', 'w') as f:
    cursor.copy_expert(outputquery, f)

DBData = read_csv('resultsfile.csv')
DBData.rename(columns={'movieid': 'A',
                       'type': 'B',
                       'startyear': 'C',
                       'runtime': 'D',
                       'avgrating': 'E',
                       'genreid': 'F',
                       'genre': 'G',
                       'memberid': 'H',
                       'birthyear': 'I',
                       'role': 'J'
                       },
                 inplace=True)

totaltuples = len(DBData.index)
listofcolumns = list(DBData.columns.values)  # returns column names

table_tuple = ['NULL'] * totaltuples  # temp table for stripped_partitions


tuple_mapping = {'NULL': listofcolumns}
partition_list = {}

# partitioning
for a in listofcolumns:
    partition_list[a] = []
    for element in equivalence_class(DBData[a].tolist()):
        if len(element[1]) > 1:
            partition_list[a].append(element[1])

functional_dependencies = []
L0 = []
L1 = listofcolumns[:]  # keeping original list as is, creating a new list
partition_index = 1  # since 0 element is null list

L = [L0, L1]

while not (L[partition_index] == []):
    get_functional_dependency(L[partition_index])
    # prune L[1]
    invalid_partitions = []
    for attribute in L[partition_index]:
        if tuple_mapping[attribute] is []:  
            L[partition_index].remove(attribute)
    for item in invalid_partitions:
        L[partition_index].remove(item)
    temp = get_next_partition(L[partition_index])
    L.append(temp)
    partition_index = partition_index + 1


listOfAttributes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
listOfOriginalAttributes = [" movieid", " type", " startyear", " runtime", " avgrating", " genreid", " genre",
                            " memberid", " birthyear", " role"]
for items in functional_dependencies:
    fdleft = ''
    fdright = ''
    for a in str(items[0]):
        index = listOfAttributes.index(a)
        fdleft += listOfOriginalAttributes[index]
    for a in str(items[1]):
        index = listOfAttributes.index(a)
        fdright += listOfOriginalAttributes[index]
    print(fdleft, "->", fdright)
print("Total: ", len(functional_dependencies))
# removing the dummy file
os.remove("resultsfile.csv")