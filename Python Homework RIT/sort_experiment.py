import random
import time
import instrumented_sort

def test_merge_sort():
    sample_size = 10
    sample_data = random.sample(range(sample_size * 5), sample_size)
    print('Sample size: ', sample_size)
    begin = time.time()
    result = instrumented_sort.msort(sample_data)[0]
    end = time.time()
    expected = sorted(sample_data)
    print('Sorting time: %f \'secs' % (end - begin))

    assert result == expected
    print(result)
    # print('Algorithm correct')


def main():
    # a_list_s = [3, 5, 4, 1, 8]
    # print(ssort(a_list_s))
    # a_list_m = [3, 5, 4, 1, 8]
    # print(msort(a_list_m))
    test_merge_sort()


if __name__ == '__main__':
    main()