# ads_proj2
___

To run the project follow this guide:

1. Clone the repository

2. Initialize the submodules with the following command
```
git submodule update --init --recursive
```

3. Navigate to the data folder of the ssb benchmark

```
cd duckdb/benchmark/ssb/data
```

4. Use the SSB generator located in the folder `ads2024-ssb-dbgen` to generate data for each scaling factor: `1`, `10` and `100`. This should produce five different `.tbl` files. Place these five files for each scaling factor in their respective folders `SF1`, `SF10` and `SF100`. (An example of generating the customer table for scaling factor 10 is seen below)

```
./dbgen -T c -s 10
```

5. Build DuckDB with the benchmark runner with the following command. Firstly, navigate to the main folder of DuckDB

```
BUILD_BENCHMARK=1 GEN=NINJA make
```

6. Navigate to the queries folder and run the benchmarks with the following command (replace `<NUM>` with your thread count):

```
cd benchmark/ssb/queries
../../../build/release/benchmark/benchmark_runner --disable-timeout --threads=<NUM> "benchmark/ssb/queries/*/.*"
```
The results will be shown in the terminal.

7. Alternatively, navigate to the main folder where this readme is placed and run the benchmark script `bench.sh`. This places the results in the resutls folder, however the files will only contain the execution times, not which query have been executed for that specific time. The benchmark runner will always execute 5 runs of each query for each scaling factor. So the file can be interpreted as:

```
query 1.1 - scaling factor 1
... 4 more execution times for query 1.1
query 2.3 - scaling factor 1
... 4 more execution times for query 2.3
query 3.4 - scaling factor 1
... 4 more execution times for query 3.4
query 1.1 - scaling factor 10
... 4 more execution times for query 1.1
and so on
```




