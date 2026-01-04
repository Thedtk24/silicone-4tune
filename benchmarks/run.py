import subprocess
import csv
import os

# =========================
# CONFIGURATION EXPÉRIENCE
# =========================

BINARY = "./run_matmul"
N = 1024

BLOCK_SIZES = [16, 32, 64, 128]
THREADS = [1, 2, 4, 8]

METRICS_DIR = "../metrics"
os.makedirs(METRICS_DIR, exist_ok=True)

# =========================
# UTILITAIRE
# =========================

def run_once(n, bs, threads):
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(threads)

    result = subprocess.run(
        [BINARY, str(n), str(bs)],
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        print("Error:", result.stderr)
        return None

    # sortie attendue : N,BS,time,gflops
    line = result.stdout.strip()
    n, bs, time_ms, gflops = line.split(",")

    return {
        "N": int(n),
        "BS": int(bs),
        "threads": threads,
        "time_ms": float(time_ms),
        "gflops": float(gflops)
    }

# =========================
# EXPÉRIENCE 1 : BLOCKING
# =========================

def experiment_blocking():
    print("Running blocking experiment...")
    results = []

    FIXED_THREADS = 4

    for bs in BLOCK_SIZES:
        res = run_once(N, bs, FIXED_THREADS)
        if res:
            results.append(res)

    output = os.path.join(METRICS_DIR, "blocking.csv")
    write_csv(output, results)

# =========================
# EXPÉRIENCE 2 : THREAD SCALING
# =========================

def experiment_thread_scaling():
    print("Running thread scaling experiment...")
    results = []

    OPTIMAL_BS = 16 

    for t in THREADS:
        res = run_once(N, OPTIMAL_BS, t)
        if res:
            results.append(res)

    output = os.path.join(METRICS_DIR, "thread_scaling.csv")
    write_csv(output, results)

# =========================
# CSV WRITER
# =========================

def write_csv(path, data):
    if not data:
        print("No data to write:", path)
        return

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["N", "BS", "threads", "time_ms", "gflops"]
        )
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print("Written:", path)

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    experiment_blocking()
    experiment_thread_scaling()
