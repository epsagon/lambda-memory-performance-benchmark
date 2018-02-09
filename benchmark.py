"""
Benchmark script.
"""

from __future__ import print_function
import os
import boto3

FUNCTION_NAME = 'lambda-performance-benchmark-dev-main'
MEMORY_SIZES = [
    128,
    192,
    256,
    512,
    768,
    1024,
    1536,
    2048,
    2560,
    3008,
]


def run_benchmark():
    """
    Run benchmark.
    :return: None.
    """

    # Deploy function.
    return_code = os.system('sls deploy')

    if return_code != 0:
        print('There was an error deploying. Aborting.')
        return

    print('-' * 20)
    lambda_client = boto3.client('lambda')
    results = {}

    # Load payloads
    with open('cold_data.json', 'rt') as input_data:
        cold_payload = input_data.read()
    with open('warm_data.json', 'rt') as input_data:
        warm_payload = input_data.read()

    for memory_size in MEMORY_SIZES:

        print('Setting memory size: {0}MB'.format(memory_size))
        lambda_client.update_function_configuration(
            FunctionName=FUNCTION_NAME,
            MemorySize=memory_size,
        )

        print('Warming Lambda')
        lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            Payload=cold_payload,
        )

        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            Payload=warm_payload,
        )
        result = '%.6f' % (float(response['Payload'].read()),)
        results[memory_size] = result
        print('Result: {0}'.format(result))

    with open('results.csv', 'wt') as output_results:
        output_results.write('Memory Size,Duration (in ms)\n')
        for memory_size in MEMORY_SIZES:
            output_results.write('{},{}\n'.format(
                '{0}MB'.format(memory_size),
                '%.2f' % (float(results[memory_size]) * 1000,)
            ))

    os.system('sls remove')


if __name__ == '__main__':
    run_benchmark()
