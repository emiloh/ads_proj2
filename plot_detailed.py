import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from pathlib import Path
import json
import sys

query_map = {"q01_1": "Query 1.1", "q02_3": "Query 2.3", "q03_4": "Query 3.4"}
sfs = ["sf1", "sf10", "sf100"]

def get_list(res):
    if not res["children"]:
        tup = (res["operator_type"], res["operator_timing"], res["operator_rows_scanned"], res["operator_cardinality"])
        return [tup]
    else:
        l = [(res["operator_type"], res["operator_timing"], res["operator_rows_scanned"], res["operator_cardinality"])]
        for i  in range(len(res["children"])):
            l += (get_list(res["children"][i]))
        return l


def retrieve_timings(query, sf, folder):
    paths = [f"{str(folder)}/detailed_{query}_{sf}_{thread}.json" for thread in [1,2,4,8]]

    data = defaultdict(list)

    for path in paths:
        with open(path, "r") as f:
            threads = path.replace(".json", "").split("_")[-1]
            res = json.loads(f.read())
            l = get_list(res["children"][0])
            data[threads] = l
    
    zipped = zip(data["1"], data["2"], data["4"], data["8"])
    
    mapped = list(map(lambda t: (t[0][0], [t[0][1], t[1][1]/2, t[2][1]/4, t[3][1]/8]), zipped))
    
    return mapped
def plot_operator_timings(folder):
    info = {"sf1": ("ms", 1000, (0, 500, 50)), "sf10": ("ms", 1000, (0, 1500, 100)), "sf100": ("ms", 1000, (0, 50, 5))}
    for query in query_map.keys():
        for sf in sfs:
            data = retrieve_timings(query, sf, folder)
            
            x_ticks = list(map(lambda x: x[0], data))

            colors = ["blue", "green", "red", "orange"]
            threads = ["Threads: 1", "Threads: 2", "Threads: 4", "Threads: 8"]
            
            y_ticks = defaultdict(list)
            y_ticks[0] = list(map(lambda x: x[1][0] * info[sf][1], data))
            y_ticks[1] = list(map(lambda x: x[1][1] * info[sf][1], data))
            y_ticks[2] = list(map(lambda x: x[1][2] * info[sf][1], data))
            y_ticks[3] = list(map(lambda x: x[1][3] * info[sf][1], data))

            # Define how many ticks there are
            x = np.arange(len(x_ticks))

            # Witdth of the bars within a bar group (x tick)
            bar_width = 0.20
    
            # Group specifier
            multiplier = 0

            fig, ax = plt.subplots()

            for i in range(4):
                offset = bar_width * multiplier
                rects = ax.bar(x + offset, y_ticks[i], bar_width, label=threads[i], color=colors[i])
                multiplier += 1

            plt.ylim((10**-2, 10**4))
           # plt.yticks(np.arange(info[sf][2][0], info[sf][2][1], info[sf][2][2]))
            plt.yscale("log")
            plt.ylabel(f"Operator execution time per thread ({info[sf][0]}) ")    
            plt.legend(loc="upper left", ncols=1)
            ax.set_xticks(x + (1.5 * bar_width), x_ticks)
            plt.xticks(rotation=90)
            fig.set_dpi(400)
            fig.set_figwidth(10)
            fig.savefig(f"operator_{query}_{sf}.pdf", format="pdf", bbox_inches="tight")




if __name__ == "__main__":
    folder = Path(sys.argv[1])
    plot_operator_timings(folder)

