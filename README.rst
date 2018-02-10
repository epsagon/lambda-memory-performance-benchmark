AWS Lambda Memory Performance Benchmark
=======================================

Motivation
----------
- Understand how RAM selection affect Lambda's performance.
- `Share insights on a blog post on Medium <https://medium.com/epsagon/how-to-make-lambda-faster-memory-performance-benchmark-be6ebc41f0fc>`_.


Setup
-----
.. code-block:: bash

    git clone git@github.com:epsagon/lambda-memory-performance-benchmark.git
    cd lambda-memory-performance-benchmark/
    pip install -r requirements.txt
    python benchmark.py


Last Result (February 9th, 2018)
--------------------------------

Chart:

.. image:: https://github.com/epsagon/lambda-memory-performance-benchmark/blob/master/performance_chart.png


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
