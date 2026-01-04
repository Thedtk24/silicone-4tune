import csv
import os
from subprocess import run

from search_space import BLOCK_SIZES, THREADS
from llm_decider import decide_next

BINARY = "../benchmarks/run_matmul"
N = 1024
BUDGET = 6

OUTPUT = "../metrics/llm_search.csv"

def run_config(bs, threads):
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(threads)

    result = run(
        [BINARY, str(N), str(bs)],
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
        "threads": threads,
        "time_ms": float(time_ms),
        "gflops": float(gflops)
    }

def main():
    history = []
    candidates = [(bs, t) for bs in BLOCK_SIZES for t in THREADS]

    for step in range(BUDGET):
        choice = decide_next(history, candidates)
        if not choice:
            break

        print(f"[LLM] Step {step+1}: testing {choice}")

        res = run_config(choice["bs"], choice["threads"])
        if res:
            history.append(res)

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["N", "BS", "threads", "time_ms", "gflops"]
        )
        writer.writeheader()
        for r in history:
            writer.writerow(r)

    print("LLM search results written to", OUTPUT)

if __name__ == "__main__":
    main()
