import sys
import os
from collections import defaultdict
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

def read_data(parent_path):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    sfs = ["SF1", "SF10", "SF100"]
    queries = ["Query 1.1", "Query 2.3", "Query 3.4"]
    for path in parent_path.rglob("THREADS*"):
        with open(path, "r") as f:
            name, thread = str(path).strip().split("_")
            numbers = f.readlines()
            sf = 0
            for i in range(0, 45, 15):
                q = 0
                for j in range(0, 15, 5):
                    data[thread][queries[q]][sfs[sf]] = sum(map(float, numbers[i+j:i+j+5]))/5
                    q += 1   
                sf += 1
    return data

def thread_plots(data, out):
    x_ticks = ["SF1", "SF10", "SF100"]
    line_names = ["Query 1.1", "Query 2.3", "Query 3.4"]
    
    for thread, data_thread in data.items():
        fig, ax = plt.subplots()
        
        colors = ["blue", "orange", "green"]
        markers = [".", "s", "x"]
        
        # Define how many ticks there are
        x = np.arange(len(x_ticks))

        # Witdth of the bars within a bar group (x tick)
        bar_width = 0.20
    
        # Group specifier
        multiplier = 0

        for i, line in enumerate(line_names):
            offset = bar_width * multiplier
            y_ticks = data_thread[line].values()
            rects = ax.bar(x + offset, y_ticks, bar_width, label=line, color=colors[i])
            multiplier += 1
            #plt.plot(x_ticks, y_ticks, marker=markers[i], color=colors[i], label=line)
        
        plt.yscale("log")
        plt.ylim((10**-2, 10**2))
        plt.ylabel("Query execution time (ms)")
        ax.set_xticks(x + (1.5 * bar_width), x_ticks)
        plt.legend(loc="upper left", ncols=1)

        fig.savefig(f"{out}/fixed_threads_{thread}.pdf", format="pdf", bbox_inches="tight")


def scaling_factor_plots(data, out):
    x_ticks = ["1", "2", "4", "8"]
    line_names = ["Query 1.1", "Query 2.3", "Query 3.4"]
    sfs = ["SF1", "SF10", "SF100"]
    y_info = [("ms", (0,220), 40, True), ("ms", (0, 2400), 400, True), ("seconds", (0, 25), 5, False)]

    for sf in range(3):
        query_data = []
        for query in line_names:
            l = []
            for thread in x_ticks:
                num = data[thread][query][sfs[sf]]
                if y_info[sf][3]:
                    num *= 1000
                l.append(num)
            query_data.append(l)
        
        print()
        print(query_data)
        fig, ax = plt.subplots()
            
        colors = ["blue", "orange", "green"]
            
        # Define how many ticks there are
        x = np.arange(len(x_ticks))

        # Witdth of the bars within a bar group (x tick)
        bar_width = 0.20
    
        # Group specifier
        multiplier = 0
        
        for i, line in enumerate(line_names):
            offset = bar_width * multiplier
            y_ticks = query_data[i]
            rects = ax.bar(x + offset, y_ticks, bar_width, label=line, color=colors[i])
            multiplier += 1
            

        plt.ylabel(f"Query execution time ({y_info[sf][0]})")
        plt.yticks(np.arange(y_info[sf][1][0], y_info[sf][1][1], y_info[sf][2]))
        plt.xlabel("Threads")
        ax.set_xticks(x + (1.5 * bar_width), x_ticks)
        plt.legend(loc="upper right", ncols=1)
        
        fig.savefig(f"{out}/fixed_sf_{sfs[sf]}.pdf", format="pdf", bbox_inches="tight")


def create_plots(parent_path, out):
    data = read_data(parent_path)
    print(data)
    thread_plots(data, out)
    scaling_factor_plots(data, out)

if __name__ == "__main__":
    path = Path(sys.argv[1])
    out = sys.argv[2]
    create_plots(path, out)
