#!/bin/bash

PROJ_HOME=/home/group10/ads_project2/ads_proj2
QUERY_HOME=$PROJ_HOME/duckdb/benchmark/ssb/queries
RESULT_HOME=$PROJ_HOME/results
THREADS=(1 2 4 8)

cd $QUERY_HOME

for thread_count in "${THREADS[@]}"
do 
	../../../build/release/benchmark/benchmark_runner --disable-timeout --threads=$thread_count --out="$RESULT_HOME/THREADS_$thread_count" "benchmark/ssb/queries/*/.*"		
done
