CC=gcc-15
CFLAGS=-O3 -fopenmp -Wall
LDFLAGS=../kernels/libkernels.a

all: run_matmul

run_matmul: run_matmul.c
	$(CC) $(CFLAGS) run_matmul.c $(LDFLAGS) -o run_matmul

clean:
	rm -f run_matmul
