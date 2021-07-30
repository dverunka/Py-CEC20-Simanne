#!/usr/bin/env python3

from ctypes import CDLL, POINTER, c_int, c_double
import matplotlib.pyplot as plt
import numpy as np
import sys

import simulated_annealing

CEC20_SO_LIB = "./cec20_test_func.so"

DIMENSION_TO_MAX_FES = {
    5: 50000,
    10: 1000000
}

BOUNDS = [-100, 100]
RUNS = 30

FUNCTIONS = {
    1: "bent_cigar", # 100
    2: "schwefel", # 1100
    3: "lunacek_bi_rastrigin", # 700
    4: "rosenbrock_griewangk", # 1900
    5: "hybrid_one", # 1700
    6: "hybrid_two", # 1600
    7: "hybrid_three", # 2100
    8: "composition_one", # 2200
    9: "composition_two", # 2400
    10: "composition_three" # 2500
}

FUNCTIONS_TO_DIMENSIONS = {
    1: [5, 10],
    2: [5, 10],
    3: [5, 10],
    4: [5, 10],
    5: [5, 10],
    6: [10],
    7: [10],
    8: [5, 10],
    9: [5, 10],
    10: [5, 10]
}

OUTPUT_DIR = "graphs/"

def init_graph(title):
    plt.xlabel("FES")
    plt.ylabel("cost function")
    plt.grid(True)
    plt.title(title)


def main():
    # Define C library interface
    cec20 = CDLL(CEC20_SO_LIB)
    cec20.cec20_test_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
    cec20.cec20_test_func.restype = None

    # Alias for C function
    cost_function = cec20.cec20_test_func

    algos = {"simanne": simulated_annealing}

    # Evaluate test functions using Simulated annealing
    global_results = {x: {y: {} for y in FUNCTIONS_TO_DIMENSIONS[x]} for x in FUNCTIONS}
    
    for func_id in FUNCTIONS:
        for dimension in FUNCTIONS_TO_DIMENSIONS[func_id]:
            for algo_name, algo_lib in algos.items():
                print(f"Starting evaluation of {algo_name}_F{func_id}_{FUNCTIONS[func_id]}_{dimension}D.")
                all_run_results = []
                best_run_results = []

                for i in range(RUNS):
                    best_results = algo_lib.run(BOUNDS, dimension, cost_function, func_id, DIMENSION_TO_MAX_FES[dimension])
                    for idx, res in enumerate(best_results):
                        if idx >= len(all_run_results):
                            all_run_results.append([])
                        all_run_results[idx].append(res)
                    sys.stdout.write(f"\rRun {i+1}/{RUNS} completed.")
                    sys.stdout.flush()
                    best_run_result = np.min(best_results)
                    best_run_results.append(best_run_result)
                print("")

                average_run_results = []
                for run_result in all_run_results:
                    average_run_result = np.mean(run_result)
                    average_run_results.append(average_run_result)
                global_results[func_id][dimension][algo_name] = average_run_results

                minimum = np.min(best_run_results)
                maximum = np.max(best_run_results)
                mean = np.mean(best_run_results)
                median = np.median(best_run_results)
                stddev = np.std(best_run_results)
                print(f"Evaluation of {FUNCTIONS[func_id]}_{dimension}D finished, min={minimum}, max={maximum}, mean={mean}, median={median}, stddev={stddev}")

    # Plot graphs
    print(f"Plotting graphs to output dir: {OUTPUT_DIR}")

    for func_id in FUNCTIONS:
        for dimension in FUNCTIONS_TO_DIMENSIONS[func_id]:
            init_graph(f"F{func_id}_{FUNCTIONS[func_id]}_{dimension}D, average best run")
            for algo_name, algo_average_run_result in global_results[func_id][dimension].items():
                plt.plot(range(1, len(algo_average_run_result)+1), algo_average_run_result, linewidth=1, label=algo_name)
            plt.savefig(f"{OUTPUT_DIR}F{func_id}_{FUNCTIONS[func_id]}_{dimension}d.png")
            plt.clf()
            plt.cla()
            plt.close()

    print("Plotting graphs finished.")


if __name__ == "__main__":
    main()
