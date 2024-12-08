import duckdb
from pathlib import Path
import sys

def run_queries_get_json(out):
    sfs = ["sf1", "sf10", "sf100"]
    queries = ["q01_1", "q02_3", "q03_4"]
    threads = [1, 2, 4, 8]

    for sf in sfs:
        db = f"duckdb/duckdb_benchmark_data/{sf}.duckdb"
        conn = duckdb.connect(db)
        
        config = """PRAGMA enable_profiling = json";
        PRAGMA custom_profiling_settings = {"OPERATOR_CARDINALITY": "true", "OPERATOR_ROWS_SCANNED": "true", "OPERATOR_TIMING": "true", "OPERATOR_TYPE": "true"};
        """

        conn.sql(config)

        for thread in threads:
            conf_threads = f"PRAGMA threads = {thread}"
            conn.sql(conf_threads)
            
            for query in queries:
                out = f"PRAGMA profiling_output = {out}/json_{query}_{sf}_{thread}.json"
                conn.sql(out)

                q = Path(f"duckdb/benchmark/ssb/queries/{query}.sql").read_text()
                conn.sql(q)


def create_operator_graphs(path):
    pass


if __name__ == "__main__":
    out = sys.argv[1]
    run_queries_get_json(out)