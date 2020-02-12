__author__ = 'BR'

"""
Author: BIKASH ROY

File name: zips_heaps_law.py
"""

'''
This python program implementation of Zipf's law and Heaps' law .

Apart from plotting graph, data is also written in xls files for better viewing of data.
'''
import xlsxwriter
import re
from operator import itemgetter
import matplotlib.pyplot as plt

regex = re.compile(r'([\w+]{2,9})')  # regex to read only words, of length 2 to 9
words = regex.findall(open('book1.txt', 'r').read())
word_cloud_base = {}
for word in words:
    word_cloud_base[word] = word_cloud_base.get(word, 0) + 1

# Check Zipf's law
print('Processing on Zipf\'s law.')
zipf_file = xlsxwriter.Workbook('Zipf.xlsx')
sheet = zipf_file.add_worksheet()
sheet.write(0, 0, 'Rank')
sheet.write(0, 1, 'Count')
sheet.write(0, 2, 'Word')
rank = 1
total_words = 0
ranks_array = []
value_array = []
for key, value in reversed(sorted(word_cloud_base.items(), key=itemgetter(1))):
    sheet.write(rank, 0, rank)
    sheet.write(rank, 1, value)
    sheet.write(rank, 2, key)
    total_words += value
    rank += 1
    ranks_array.append(rank)
    value_array.append(value)
zipf_file.close()
plt.plot(ranks_array[:200], value_array[:200])
plt.ylabel('value_array')
plt.xlabel('ranks_array')
plt.title('value_array V/S ranks_array')
plt.show()


# Check Heaps' law
print('Processing on Heaps\' law.')
unique_count = 0
total_count = 0
unique_count_array = []
total_count_array = []
unique_words = []
for word in words:
    total_count += 1
    if word not in unique_words:
        unique_count += 1
        unique_words.append(word)
    unique_count_array.append(unique_count)
    total_count_array.append(total_count)
plt.plot(total_count_array, unique_count_array)
plt.ylabel('unique_count_array')
plt.xlabel('total_count_array')
plt.title('unique_count_array V/S total_count_array')
plt.show()

heaps_file = xlsxwriter.Workbook('Heaps.xlsx')
sheet = heaps_file.add_worksheet()
sheet.write(0, 0, 'Unique Word Count')
sheet.write(0, 1, 'Total words in texts')
sheet.write(1, 0, len(word_cloud_base))
sheet.write(1, 1, sum(word_cloud_base.values()))
heaps_file.close()
print('\nProcess completed. \n Files Created!')
print('Total words count: ' + str(total_words) + '\n')
