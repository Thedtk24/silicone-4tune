#include "matmul.h"

void matmul_blocked(const double* A, const double* B, double* C, int N, int BS) {
    for (int ii = 0; ii < N; ii += BS)
        for (int jj = 0; jj < N; jj += BS)
            for (int kk = 0; kk < N; kk += BS)
                for (int i = ii; i < ii + BS; i++)
                    for (int j = jj; j < jj + BS; j++) {
                        double sum = C[i*N + j];
                        for (int k = kk; k < kk + BS; k++)
                            sum += A[i*N + k] * B[k*N + j];
                        C[i*N + j] = sum;
                    }
}
