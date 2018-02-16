AWS Lambda Memory Performance Benchmark
=======================================

Motivation
----------
- Understand how RAM selection affect Lambda's performance (on `Medium <https://medium.com/epsagon/how-to-make-lambda-faster-memory-performance-benchmark-be6ebc41f0fc>`_).
- Code a tool that measures Lambda function performance (duration and cost) with several memory sizes.


Setup
-----
.. code-block:: bash

    git clone git@github.com:epsagon/lambda-memory-performance-benchmark.git
    cd lambda-memory-performance-benchmark/
    pip install -r requirements.txt
    python benchmark.py -f <function_name> -r <function_region> -p <payload_filename>


Usage
-----

Basic run:

.. code-block:: bash

    python benchmark.py -f lambda-performance-benchmark -r us-east-1 -p fibonacci-function/payload.json


Fibonacci's Last Result (February 9th, 2018)
--------------------------------

Chart:

.. image:: https://github.com/epsagon/lambda-memory-performance-benchmark/blob/master/fibonacci-function/performance_chart.png


Table:

 ============= ==================
  Memory Size   Duration (in ms)
 ============= ==================
  128MB                   376.05
  192MB                   250.24
  256MB                   198.56
  512MB                    98.36
  768MB                    65.48
  1024MB                   45.31
  1536MB                   30.53
  2048MB                   25.21
  2560MB                   25.36
  3008MB                   25.15
 ============= ==================
