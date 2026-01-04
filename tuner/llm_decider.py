def decide_next(history, candidates):
    """
    history: list of dicts with keys: BS, threads, gflops
    candidates: list of (BS, threads) not yet tested
    """

    # 1. Si aucune donnée → point médian
    if not history:
        return {"bs": 16, "threads": 4}

    # 2. Trouver la meilleure config connue
    best = max(history, key=lambda x: x["gflops"])

    best_bs = best["BS"]
    best_threads = best["threads"]

    # 3. Heuristique HPC (raisonnement)
    # - si plus de threads améliore → continuer à monter
    # - si BS plus petit améliore → explorer plus petit

    tested = {(h["BS"], h["threads"]) for h in history}

    # Candidats proches
    neighbors = []

    for bs, t in candidates:
        if abs(bs - best_bs) <= best_bs and abs(t - best_threads) <= best_threads:
            neighbors.append((bs, t))

    # Priorité : plus de threads
    for bs, t in sorted(neighbors, key=lambda x: (-x[1], abs(x[0] - best_bs))):
        if (bs, t) not in tested:
            return {"bs": bs, "threads": t}

    # Fallback
    for bs, t in candidates:
        if (bs, t) not in tested:
            return {"bs": bs, "threads": t}

    return None
