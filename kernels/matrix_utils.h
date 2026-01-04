#ifndef MATRIX_UTILS_H
#define MATRIX_UTILS_H

#pragma once
#include <stddef.h>

double* alloc_matrix(int N);
void init_matrix(double* M, int N);
void zero_matrix(double* M, int N);
int compare_matrices(const double* A, const double* B, int N);


#endif