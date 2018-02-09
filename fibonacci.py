"""
Lambda function for performance benchmark.
"""

from __future__ import print_function
import time
import json

TESTS = 100


def fibonacci(index):
    """
    Recursive function that calculates Fibonacci sequence.
    :param index: the n-th element of Fibonacci sequence to calculate.
    :return: n-th element of Fibonacci sequence.
    """

    if index <= 1:
        return index
    return fibonacci(index - 1) + fibonacci(index - 2)


def handler(event, _):
    """
    Main handler.
    :param event: event data.
    :param _: unused context.
    :return: average duration.
    """
    start_time = time.time()
    for _ in range(TESTS):
        fibonacci(event['index'])
    duration = time.time() - start_time
    return duration / TESTS


def test_locally():
    """
    Testing locally.
    :return: None.
    """
    with open('warm_data.json', 'rt') as input_data:
        data = json.load(input_data)
    print(handler(data, None))


if __name__ == '__main__':
    test_locally()
