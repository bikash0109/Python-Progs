def ssort(unsorted_list):
    number_of_comparisons = 0
    for i in range(len(unsorted_list)):
        min_idx = i
        for j in range(i + 1, len(unsorted_list)):
            number_of_comparisons += 1
            if unsorted_list[min_idx] > unsorted_list[j]:
                min_idx = j

        unsorted_list[i], unsorted_list[min_idx] = unsorted_list[min_idx], unsorted_list[i]

    return unsorted_list, number_of_comparisons


def msort(unsorted_list):
    number_of_comparisons = 0

    if len(unsorted_list) > 1:
        mid_index = len(unsorted_list) // 2
        left = unsorted_list[:mid_index]
        right = unsorted_list[mid_index:]

        left_part_with_no_of_comparison = msort(left)
        right_part_with_no_of_comparison = msort(right)

        number_of_comparisons += left_part_with_no_of_comparison[1] + right_part_with_no_of_comparison[1]

        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            number_of_comparisons += 1
            if left[i] < right[j]:
                unsorted_list[k] = left[i]
                i = i + 1

            else:
                unsorted_list[k] = right[j]
                j = j + 1

            k = k + 1

        while i < len(left):
            unsorted_list[k] = left[i]
            i = i + 1
            k = k + 1
            number_of_comparisons += 1

        while j < len(right):
            unsorted_list[k] = right[j]
            j = j + 1
            k = k + 1
            number_of_comparisons += 1

    return unsorted_list, number_of_comparisons


# Function to do insertion sort
def isort(unsorted_list):
    k = 0
    comparisons = 0
    while k + 1 <= len(unsorted_list) - 1:
        index = k + 1
        curr_val = unsorted_list[index]
        comparisons += 1
        while index > 0 and unsorted_list[index - 1] > curr_val:
            unsorted_list[index] = unsorted_list[index - 1]
            index = index - 1
            comparisons += 1
            unsorted_list[index] = curr_val
        k = k + 1
    return unsorted_list, comparisons


def partition(unsorted_list, start, end, number_of_comparisons):
    pos = start
    for i in range(start, end):
        number_of_comparisons += 1
        if unsorted_list[i] < unsorted_list[end]:
            unsorted_list[i], unsorted_list[pos] = unsorted_list[pos], unsorted_list[i]
            pos += 1
    unsorted_list[pos], unsorted_list[end] = unsorted_list[end], unsorted_list[pos]
    return pos, number_of_comparisons


def quick_sort(unsorted_list, start, end, number_of_comparisons):
    if start < end:
        pos, number_of_comparisons = partition(unsorted_list, start, end, number_of_comparisons)
        number_of_comparisons = quick_sort(unsorted_list, start, pos - 1, number_of_comparisons)
        number_of_comparisons = quick_sort(unsorted_list, pos + 1, end, number_of_comparisons)
    return number_of_comparisons


def qsort(unsorted_list):
    number_of_comparisons = quick_sort(unsorted_list, 0, len(unsorted_list) - 1, 0)
    return unsorted_list, number_of_comparisons