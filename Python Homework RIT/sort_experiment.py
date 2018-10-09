import random
import time
import instrumented_sort


def test_selection_sort(sample_size, sample_data):
    begin = time.time()
    output = instrumented_sort.ssort(sample_data)
    result = output[0]
    comparison = output[1]
    end = time.time()
    time_taken = end - begin

    print('Algorithm', '\t\t\tN', '\t\t\tComparison', '\t\t\tSeconds')
    print('\nSelection Sort', '\t\t\t', sample_size, '\t\t\t', comparison, '\t\t\t%f secs' % time_taken)
    expected = sorted(sample_data)
    assert result == expected


def test_merge_sort(sample_size, sample_data):
    begin = time.time()
    output = instrumented_sort.msort(sample_data)
    result = output[0]
    comparison = output[1]
    end = time.time()
    time_taken = end - begin

    print('\nMerge Sort', '\t\t\t', sample_size, '\t\t\t', comparison, '\t\t\t%f secs' % time_taken)
    expected = sorted(sample_data)
    assert result == expected


def test_insertion_sort(sample_size, sample_data):
    begin = time.time()
    output = instrumented_sort.isort(sample_data)
    result = output[0]
    comparison = output[1]
    end = time.time()
    time_taken = end - begin

    print('\nInsertion Sort', '\t\t\t', sample_size, '\t\t\t', comparison, '\t\t\t%f secs' % time_taken)
    expected = sorted(sample_data)
    assert result == expected


def test_quick_sort(sample_size, sample_data):
    begin = time.time()
    output = instrumented_sort.qsort(sample_data)
    result = output[0]
    comparison = output[1]
    end = time.time()
    time_taken = end - begin

    print('\nQuick Sort', '\t\t\t', sample_size, '\t\t\t', comparison, '\t\t\t%f secs' % time_taken)
    expected = sorted(sample_data)
    assert result == expected


def test_sort(n):
    sample_size = n
    sample_data = random.sample(range(sample_size * 5), sample_size)
    test_selection_sort(sample_size, sample_data)
    test_merge_sort(sample_size, sample_data)
    test_insertion_sort(sample_size, sample_data)
    test_quick_sort(sample_size, sample_data)


def main():
    # for i in [1, 10, 100, 1000, 10000]:
        test_sort(990)


if __name__ == '__main__':
    main()
