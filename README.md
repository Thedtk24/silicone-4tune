# Silicone 4Tune — HPC Kernel Autotuning Guided by LLM

## 1. Projet

**Nom** : Silicone 4Tune — HPC kernel autotuning guided by a reasoning LLM

**Objectif** :  
- Étudier les performances d’un kernel de multiplication de matrices sur Apple Silicon  
- Comparer trois stratégies d’autotuning :  
  1. Grid Search  
  2. Random Search  
  3. LLM-guided search

**Contexte** :  
- Kernels implémentés en C (naïf, blocked, blocked + OpenMP)  
- Benchmark et mesures avec Python  
- LLM simulé pour guider l’autotuning sans générer de code, uniquement par raisonnement sur l’historique

---

## 2. Structure du projet
```text
Silicone4Tune/
├── benchmarks/
│   ├── run_matmul.c
│   ├── run.py
│   └── timer.h
├── kernels/
│   ├── matmul_naive.c
│   ├── matmul_blocked.c
│   ├── matmul_blocked_omp.c
│   ├── matrix_utils.c/h
│   └── Makefile
├── metrics/
│   ├── blocking.csv
│   ├── thread_scaling.csv
│   ├── random_search.csv
│   ├── grid_search.csv
│   └── llm_search.csv
├── tuner/
│   ├── search_space.py
│   ├── random_search.py
│   ├── grid_search.py
│   ├── llm_decider.py
│   └── llm_tuner.py
├── docs/
│   └── Silicone 4Tune-v1.pdf
├── reports/
└── README.md
```
---

## 3. Kernels HPC

### Implémentations

- `naive` : triple boucle standard  
- `blocked` : blocage cache-friendly  
- `blocked + OpenMP` : parallélisation multi-threads  

### Observations

- Blocking **petit** optimal (BS=16)  
- Scaling threads limité par **memory-bound**  
- Apple M4 exploité efficacement

---

## 4. Résultats expérimentaux

### 4.1 Effet du BLOCK_SIZE (threads fixes = 4)

| BS  | GFLOPS |
|-----|--------|
| 16  | 19.21  |
| 32  | 12.27  |
| 64  | 7.05   |
|128  | 6.51   |

**Analyse** :  
- BS trop grand → working set dépasse cache → GFLOPS chute  
- BS=16 → meilleure localité

---

### 4.2 Effet du nombre de threads (BS=16)

| Threads | GFLOPS |
|---------|--------|
| 1       | 5.24   |
| 2       | 9.04   |
| 4       | 20.93  |
| 8       | 23.92  |

**Analyse** :  
- Scaling sous-linéaire → memory-bound  
- Saturation à 8 threads

---

### 4.3 Autotuning — comparaison

| Méthode        | Max GFLOPS | Runs |
|----------------|------------|------|
| Grid Search    | 23.83      | 12   |
| Random Search  | 25.08      | 12   |
| LLM-guided     | 24.90      | 6    |

**Observation** :  
- Grid Search trouve optimum mais coûte cher  
- Random Search variance importante  
- LLM-guided atteint presque optimum avec **moitié moins de runs**

---

### 4.4 LLM-guided search

| BS  | Threads | GFLOPS |
|-----|---------|--------|
| 16  | 4       | 20.17  |
| 16  | 8       | 24.50  |
| 8   | 8       | 24.90  |
| 8   | 4       | 18.79  |
| 8   | 2       | 9.85   |
| 16  | 2       | 8.50   |

**Analyse** :  
- LLM explore d’abord threads → augmente GFLOPS  
- Puis explore BS plus petit → atteint max GFLOPS  
- Convergence rapide (6 runs)

---

## 5. Interprétation scientifique

- Le **kernel est memory-bound**  
- **Blocking optimal faible** (cache-friendly)  
- **LLM agit comme un agent de raisonnement**, pas comme générateur de code  
- **Démonstration** : LLM atteint le max presque optimal avec moitié moins de runs que grid search

---

## 6. Instructions pour reproduire

```bash
# Compiler kernels
cd kernels
make

# Benchmark
cd ../benchmarks
make
python3 run.py

# Autotuning
cd ../tuner
python3 grid_search.py
python3 random_search.py
python3 llm_tuner.py
```