"""
Benchmark tool for measuring Lambda function performance in different memory
sizes.
"""

from __future__ import print_function
import argparse
import math
import base64
import boto3

MEMORY_TO_PRICE = {
    128: 0.000000208,
    256: 0.000000417,
    512: 0.000000834,
    1024: 0.000001667,
    1536: 0.000002501,
    2048: 0.000003334,
    2560: 0.000004168,
    3008: 0.000004897,
}
PRICE_INTERVAL = 100
INVOCATIONS_COUNT = 5
CSV_HEADER = 'Memory Size,Duration (in ms),Price Per 1M Invocations (in $)\n'


def invoke_lambda_and_get_duration(lambda_client, payload, function_name):
    """
    Invokes Lambda and return the duration.
    :param lambda_client: Lambda client.
    :param payload: payload to send.
    :param function_name: function name.
    :return: duration.
    """
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=payload,
    )

    # Extract duration from Lambda log
    lambda_log = base64.b64decode(response['LogResult']).decode('utf-8')
    report_data = \
        [line for line in lambda_log.split('\n')
         if line.startswith('REPORT')
        ][0]
    duration = \
        [col for col in report_data.split('\t')
         if col.startswith('Duration')
         ][0]
    duration = float(duration.split()[1])
    return duration


def run_benchmark(args):
    """
    Run benchmark.
    :param args: arguments.
    :return: None.
    """

    if args.aws_profile:
        aws_session = boto3.Session(profile_name=args.aws_profile)
    else:
        aws_session = boto3.Session()

    lambda_client = aws_session.client('lambda', region_name=args.region)
    sorted_memory_sizes = sorted(MEMORY_TO_PRICE)
    results = {}

    # Load payload
    with open(args.payload_file, 'rt') as input_data:
        payload = input_data.read()

    # Read Original memory size
    original_memory_size = lambda_client.get_function_configuration(
        FunctionName=args.function_name,
    )['MemorySize']
    print('Original memory size: {0}'.format(original_memory_size))

    # Benchmark
    for memory_size in sorted_memory_sizes:
        print('Setting memory size: {0}MB'.format(memory_size))
        lambda_client.update_function_configuration(
            FunctionName=args.function_name,
            MemorySize=memory_size,
        )

        print('Warming Lambda')
        lambda_client.invoke(
            FunctionName=args.function_name,
            Payload=payload,
        )

        # Run several times
        duration_sum = 0
        for _ in range(INVOCATIONS_COUNT):
            duration_sum += invoke_lambda_and_get_duration(
                lambda_client,
                payload,
                args.function_name
            )

        duration = duration_sum / INVOCATIONS_COUNT
        results[memory_size] = duration
        print('Result: {0}'.format(duration))
        print('-' * 20)

    print('Restoring original memory size')
    lambda_client.update_function_configuration(
        FunctionName=args.function_name,
        MemorySize=original_memory_size,
    )

    with open(args.output_file, 'wt') as output_results:
        output_results.write(CSV_HEADER)
        for memory_size in sorted_memory_sizes:
            price = math.ceil(results[memory_size] / PRICE_INTERVAL) \
                    * MEMORY_TO_PRICE[memory_size] * 1000000

            output_results.write('{0},{1},{2}\n'.format(
                '{0}MB'.format(memory_size),
                '%.2f' % (results[memory_size],),
                '%.2f' % (price,),
            ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Benchmark Lambda function with several memory sizes to' +
        'understand the impact on performance.'
    )

    parser.add_argument(
        '-f',
        '--function',
        dest='function_name',
        default=False,
        required=True,
        help='Tested function name.'
    )
    parser.add_argument(
        '-r',
        '--region',
        dest='region',
        default=False,
        required=True,
        help='Tested function region.'
    )
    parser.add_argument(
        '-p',
        '--payload_file',
        dest='payload_file',
        default=False,
        required=True,
        help='JSON Payload filename to send to the function.'
    )
    parser.add_argument(
        '--profile',
        dest='aws_profile',
        default=False,
        required=False,
        help='A specific AWS Named Profile configured within your AWS Credentials file.'
    )
    parser.add_argument(
        '--output',
        dest='output_file',
        default='results.csv',
        help='Output results filename.'
    )

    arguments = parser.parse_args()
    run_benchmark(arguments)
