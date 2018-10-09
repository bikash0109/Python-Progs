__author__ = 'BR'
__author__ = 'TB'

"""
Author: BIKASH ROY (Username - br8376)
Author: TANAY BHARDWAJ (Username - tb7315)

File name: sort_experiment.py
"""

import random
import time
import instrumented_sort
import sys


def generate_data(n):
    """
        Method to generate list of number, given N as the range.
        :parameter: n - the number of elements to be generated
        :return: the unsorted list of numbers.
    """
    return random.sample(range(n * 5), n)


def check_sorted(data):
    """
        Method to check if a given list is sorted in ascending order or not
        :parameter: data - the list to be checked
        :return: true/false.
    """
    previous = data[0]
    for number in data:
        if number < previous:
            return False
        previous = number
    return True


def clock_ssort(sample_data, sample_size):
    """
        Method to perform selection sort under timer.
        :parameter: sample_data - the list, which is to be sorted
        :parameter: sample_size - the size, which is to be printed
         :return: the sorted list, the number of comparisons done and time taken
    """
    begin = time.time()
    comparison = instrumented_sort.ssort(sample_data)[1]
    end = time.time()
    time_taken = end - begin
    return "\nSelection Sort\t\t\t\t\t%d%25d%30fsecs" % (sample_size, comparison, time_taken)


def clock_msort(sample_data, sample_size):
    """
        Method to perform merge sort under timer.
        :parameter: sample_data - the list, which is to be sorted
        :parameter: sample_size - the size, which is to be printed
         :return: the sorted list, the number of comparisons done and time taken
    """
    begin = time.time()
    comparison = instrumented_sort.msort(sample_data)[1]
    end = time.time()
    time_taken = end - begin
    return "\nMerge Sort\t\t\t\t\t\t%d%25d%30fsecs" % (sample_size, comparison, time_taken)


def clock_isort(sample_data, sample_size):
    """
        Method to perform insertion sort under timer.
        :parameter: sample_data - the list, which is to be sorted
        :parameter: sample_size - the size, which is to be printed
         :return: the sorted list, the number of comparisons done and time taken
    """
    begin = time.time()
    comparison = instrumented_sort.isort(sample_data)[1]
    end = time.time()
    time_taken = end - begin
    return "\nInsertion Sort\t\t\t\t\t%d%25d%30fsecs" % (sample_size, comparison, time_taken)


def clock_qsort(sample_data, sample_size):
    """
        Method to perform quick sort under timer.
        :parameter: sample_data - the list, which is to be sorted
        :parameter: sample_size - the size, which is to be printed
        :return: the sorted list, the number of comparisons done and time taken
    """
    begin = time.time()
    comparison = instrumented_sort.qsort(sample_data)[1]
    end = time.time()
    time_taken = end - begin
    return "\nQuick Sort\t\t\t\t\t\t%d%25d%30fsecs" % (sample_size, comparison, time_taken)


def output_to_file():
    """
        Method to write experiment data to the text file.
        :return: none
    """
    output_filename = "observations.txt"
    output_list = "Algorithm\t\t\t\t\t\tN\t\t\t\t\t\tComparison\t\t\t\t\t\tSeconds"
    for n in [1, 10, 100, 1000, 10000]:
        sample_data = generate_data(n)
        output_list += clock_qsort(sample_data, n)
        output_list += clock_ssort(sample_data, n)
        output_list += clock_msort(sample_data, n)
        output_list += clock_isort(sample_data, n)
        output_list += "\n****************************************************************************************" \
                       "**************************"
    try:
        with open(output_filename, "w") as output_file:
            output_file.write(str(output_list))
    except FileNotFoundError as fnf:
        print(fnf)


def main():
    """
        The main method.
        Arguments are taken in form the command line.
    """
    arguments = sys.argv
    n = int(arguments[1])
    if n < 0:
        print("Enter a positive number.")
        return
    print("Printing result for entered N.")
    print("Algorithm\t\t\t\t\t\tN\t\t\tComparison\t\t\tSeconds")
    sample_data = generate_data(n)
    output_list = ""
    output_list += clock_qsort(sample_data, n)
    output_list += clock_ssort(sample_data, n)
    output_list += clock_msort(sample_data, n)
    output_list += clock_isort(sample_data, n)
    print(output_list)
    print("*************************************************************************************************")

    print("Printing results to generate and check sort.")
    print("Calling Selection sort:")
    print("Given an unsorted data below as:")
    unsorted_data_for_selection_sort = generate_data(15)
    print(unsorted_data_for_selection_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_selection_sort))
    print("Sorting data...")
    instrumented_sort.ssort(unsorted_data_for_selection_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_selection_sort))
    print(unsorted_data_for_selection_sort)
    print("*************************************************************************************************")

    print("Calling Merge sort:")
    print("Given an unsorted data below as:")
    unsorted_data_for_merge_sort = generate_data(15)
    print(unsorted_data_for_merge_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_merge_sort))
    print("Sorting data...")
    instrumented_sort.msort(unsorted_data_for_merge_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_merge_sort))
    print(unsorted_data_for_merge_sort)
    print("*************************************************************************************************")

    print("Calling Insertion sort:")
    print("Given an unsorted data below as:")
    unsorted_data_for_insertion_sort = generate_data(15)
    print(unsorted_data_for_insertion_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_insertion_sort))
    print("Sorting data...")
    instrumented_sort.isort(unsorted_data_for_insertion_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_insertion_sort))
    print(unsorted_data_for_insertion_sort)
    print("*************************************************************************************************")

    print("Calling Quick sort:")
    print("Given an unsorted data below as:")
    unsorted_data_for_quick_sort = generate_data(15)
    print(unsorted_data_for_quick_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_quick_sort))
    print("Sorting data...")
    instrumented_sort.qsort(unsorted_data_for_quick_sort)
    print("Check if its sorted:  Calling check_sorted() :", check_sorted(unsorted_data_for_quick_sort))
    print(unsorted_data_for_quick_sort)
    print("*************************************************************************************************")

    print("Printing ... Observation.txt file for [1,10,100,1000,10000] N data for all the sort algorithms.")
    output_to_file()
    print("Printing done!")


if __name__ == '__main__':
    main()
