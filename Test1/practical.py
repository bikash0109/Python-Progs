import sys


def file_to_list(filename):
    with open(filename, "r") as file_content:
        file_array = file_content.readlines()

    array_to_string = ""
    for i in range(len(file_array)):
        array_to_string += file_array[i].replace('\n', ' ')

    array_list = array_to_string.split(" ")
    return array_list


def msort(unsorted_list):
    if len(unsorted_list) > 1:
        mid_index = len(unsorted_list) // 2
        left = unsorted_list[:mid_index]
        right = unsorted_list[mid_index:]

        msort(left)
        msort(right)

        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
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

        while j < len(right):
            unsorted_list[k] = right[j]
            j = j + 1
            k = k + 1

    return unsorted_list


def linear_search(list_to_be_searched, word_to_be_searched):
    for i in range(len(list_to_be_searched)):
        if list_to_be_searched[i] == word_to_be_searched:
            return i


def main():
    arguments = sys.argv
    if len(arguments) < 2:
        print("Enter file name: ")
        return
    filename = arguments[1]
    flag = ".txt" in filename
    if flag is False:
        print("File extension is missing: ")
        return
    list_to_be_sorted = file_to_list(filename)
    word_to_be_searched = list_to_be_sorted[10]
    msort(list_to_be_sorted)
    index = linear_search(list_to_be_sorted, word_to_be_searched)
    print(index)


if __name__ == '__main__':
  main()
