import csv
import os
from subprocess import run

from search_space import all_configs

BINARY = "../benchmarks/run_matmul"
N = 1024

OUTPUT = "../metrics/grid_search.csv"

def run_config(cfg):
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(cfg["threads"])

    result = run(
        [BINARY, str(N), str(cfg["bs"])],
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        return None

    n, bs, time_ms, gflops = result.stdout.strip().split(",")

    return {
        "N": int(n),
        "BS": int(bs),
        "threads": cfg["threads"],
        "time_ms": float(time_ms),
        "gflops": float(gflops)
    }

def main():
    results = []

    for cfg in all_configs():
        print("Testing", cfg)
        res = run_config(cfg)
        if res:
            results.append(res)

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["N", "BS", "threads", "time_ms", "gflops"]
        )
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print("Grid search results written to", OUTPUT)

if __name__ == "__main__":
    main()
