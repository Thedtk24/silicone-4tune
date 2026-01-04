CC=gcc-15
CFLAGS=-O3 -fopenmp -Wall

OBJS = matmul_naive.o matmul_blocked.o matmul_blocked_omp.o matrix_utils.o

all: libkernels.a

libkernels.a: $(OBJS)
	ar rcs libkernels.a $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.a
