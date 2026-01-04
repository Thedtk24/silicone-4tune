#include "../kernels/matmul.h"
#include "../kernels/matrix_utils.h"
#include "timer.h"
#include <stdio.h>
#include <stdlib.h>

#define RUNS 5

int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Usage: %s N BLOCK_SIZE\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    int BS = atoi(argv[2]);

    if (N % BS != 0) {
        printf("Error: N must be divisible by BLOCK_SIZE\n");
        return 1;
    }

    double* A = alloc_matrix(N);
    double* B = alloc_matrix(N);
    double* C = alloc_matrix(N);

    init_matrix(A, N);
    init_matrix(B, N);
    zero_matrix(C, N);
    matmul_blocked_omp(A, B, C, N, BS);


    double t0 = now_ms();
    for (int r = 0; r < RUNS; r++) {
        zero_matrix(C, N);
        matmul_blocked_omp(A, B, C, N, BS);
    }
    double t1 = now_ms();

    double avg = (t1 - t0) / RUNS;
    double gflops = (2.0 * N * N * N) / (avg * 1e6);

    printf("%d,%d,%.3f,%.2f\n", N, BS, avg, gflops);
}
