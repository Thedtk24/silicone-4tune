#ifndef MATMUL_H
#define MATMUL_H

#pragma once

void matmul_naive(const double* A, const double* B, double* C, int N);
void matmul_blocked(const double* A, const double* B, double* C, int N, int BS);
void matmul_blocked_omp(const double* A, const double* B, double* C, int N, int BS);


#endif