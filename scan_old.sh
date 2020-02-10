#!/bin/bash

for value in {1..10}
do
  python contest_benchmark.py | python process_results.py old_stats.txt
done
