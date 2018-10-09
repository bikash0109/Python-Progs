import random
import time
import instrumented_sort


def generate_data(n):
    return random.sample(range(n * 5), n)


def check_sorted(data):
    previous = data[0]
    for number in data:
        if number < previous:
            return False
        previous = number
    return True


def main():
    data = generate_data(1000)
    print(data)
    instrumented_sort.qsort(data)
    print(check_sorted(data))


if __name__ == '__main__':
    main()
