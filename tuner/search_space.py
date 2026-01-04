BLOCK_SIZES = [8, 16, 32]
THREADS = [1, 2, 4, 8]

def all_configs():
    configs = []
    for bs in BLOCK_SIZES:
        for t in THREADS:
            configs.append({
                "bs": bs,
                "threads": t
            })
    return configs
