import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# =============================
# Chargement des données
# =============================
blocking = pd.read_csv("metrics/blocking.csv")
threads = pd.read_csv("metrics/thread_scaling.csv")
grid = pd.read_csv("metrics/grid_search.csv")
random_search = pd.read_csv("metrics/random_search.csv")
llm = pd.read_csv("metrics/llm_search.csv")

# =============================
# Fonction utilitaire pour annotations
# =============================
def annotate_max(ax, x, y, label_offset=1.0):
    max_idx = y.idxmax()
    ax.annotate(
        f'Max: {y[max_idx]:.2f} GFLOPS',
        xy=(x[max_idx], y[max_idx]),
        xytext=(x[max_idx], y[max_idx]+label_offset),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize=10
    )

# =============================
# Création du PDF final
# =============================
pdf_path = "reports/report.pdf"
with PdfPages(pdf_path) as pdf:

    # ---- Page 1 : Titre ----
    plt.figure(figsize=(8,10))
    plt.axis('off')
    plt.text(0.5, 0.7, "Silicone 4Tune", fontsize=32, ha='center', weight='bold')
    plt.text(0.5, 0.6, "HPC Kernel Autotuning Guided by LLM", fontsize=18, ha='center')
    plt.text(0.5, 0.5, "Apple Silicon M4 — Baseline + Autotuning", fontsize=14, ha='center')
    plt.text(0.5, 0.35, "Generated PDF Report", fontsize=12, ha='center', style='italic')
    pdf.savefig()
    plt.close()

    # ---- Page 2 : Effet du Blocking ----
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(blocking["BS"], blocking["gflops"], marker='o', color='blue', label='GFLOPS')
    annotate_max(ax, blocking["BS"], blocking["gflops"])
    ax.set_title("Effect of BLOCK_SIZE on GFLOPS (threads=4)")
    ax.set_xlabel("BLOCK_SIZE")
    ax.set_ylabel("GFLOPS")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    # Texte explicatif
    ax.text(0.05, 5.5, "Observation:\n- BS trop grand → cache misses\n- BS=16 optimal", color='black', fontsize=10)
    pdf.savefig()
    plt.close()

    # ---- Page 3 : Thread Scaling ----
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(threads["threads"], threads["gflops"], marker='o', color='green', label='GFLOPS')
    annotate_max(ax, threads["threads"], threads["gflops"])
    ax.set_title("Thread Scaling (BS=16)")
    ax.set_xlabel("Number of Threads")
    ax.set_ylabel("GFLOPS")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    ax.text(1, 6, "Observation:\n- Scaling sous-linéaire\n- Memory-bound\n- Saturation à 8 threads", fontsize=10)
    pdf.savefig()
    plt.close()

    # ---- Page 4 : Grid vs Random Search ----
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(grid["threads"] + grid["BS"]/1000, grid["gflops"], 'o-', color='orange', label="Grid Search")
    ax.plot(random_search["threads"] + random_search["BS"]/1000, random_search["gflops"], 's-', color='purple', label="Random Search")
    ax.set_title("Autotuning Comparison")
    ax.set_xlabel("Threads + scaled BLOCK_SIZE")
    ax.set_ylabel("GFLOPS")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    ax.text(1, 15, "Observation:\n- Grid exhaustive mais coûteux\n- Random variable\n- Max ~25 GFLOPS", fontsize=10)
    pdf.savefig()
    plt.close()

    # ---- Page 5 : LLM-guided search ----
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(llm["threads"] + llm["BS"]/1000, llm["gflops"], 'o-', color='red', label="LLM-guided")
    annotate_max(ax, llm["threads"] + llm["BS"]/1000, llm["gflops"], label_offset=0.5)
    for i, row in llm.iterrows():
        ax.text(row["threads"] + row["BS"]/1000 + 0.01, row["gflops"]+0.3, f'BS={row["BS"]}, T={row["threads"]}', fontsize=8)
    ax.set_title("LLM-guided Autotuning")
    ax.set_xlabel("Threads + scaled BLOCK_SIZE")
    ax.set_ylabel("GFLOPS")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    ax.text(1, 9, "Observation:\n- LLM converge rapidement\n- Utilise reasoning sur l’historique\n- Atteint max GFLOPS avec moitié moins de runs", fontsize=10)
    pdf.savefig()
    plt.close()

    # ---- Page 6 : Summary Table ----
    plt.figure(figsize=(8,6))
    plt.axis('off')
    plt.title("Summary of Max GFLOPS", fontsize=16)
    summary_text = (
        "Method          Max GFLOPS\n"
        "Grid Search     {:.2f}\n"
        "Random Search   {:.2f}\n"
        "LLM-guided      {:.2f}\n\n"
        "Conclusions:\n"
        "- LLM-guided atteint rapidement la performance optimale.\n"
        "- Grid Search coûteux mais stable.\n"
        "- Random Search peu fiable.\n"
        "- BS optimal faible, threads 8 maximisent GFLOPS.\n"
    ).format(
        grid["gflops"].max(),
        random_search["gflops"].max(),
        llm["gflops"].max()
    )
    plt.text(0.05, 0.5, summary_text, fontsize=12)
    pdf.savefig()
    plt.close()

print(f"Final PDF report generated: {pdf_path}")
