#include "matrix_utils.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define ALIGN 64

double* alloc_matrix(int N) {
    double* ptr = NULL;
    posix_memalign((void**)&ptr, ALIGN, sizeof(double) * N * N);
    return ptr;
}

void init_matrix(double* M, int N) {
    for (int i = 0; i < N*N; i++)
        M[i] = (double)(i % 100) / 100.0;
}

void zero_matrix(double* M, int N) {
    memset(M, 0, sizeof(double) * N * N);
}

int compare_matrices(const double* A, const double* B, int N) {
    for (int i = 0; i < N*N; i++) {
        if (fabs(A[i] - B[i]) > 1e-9)
            return 0;
    }
    return 1;
}
