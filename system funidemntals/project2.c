#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <omp.h>

int ARRAY_SIZE  = 1000000;
int MODULO_SIZE = 1000;

int main(int argc, char** argv) {
    // Initialize random seed
    srand(12345);

    // Allocate memory for the array of random integers
    int* array = (int*)malloc(ARRAY_SIZE * sizeof(int));

    // Generate the array of random integers
    for (int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = rand();
    }

    // Start timing the parallel portion to calculate time
    struct timeval start_time, end_time;
    gettimeofday(&start_time, NULL);

    // Set the number of threads to use
    omp_set_num_threads(4); // adjust as needed

    // Process each element of the array in parallel
    #pragma omp parallel for
    for (int i = 0; i < ARRAY_SIZE; i++) {
        for (int j = 1; j <= MODULO_SIZE; j++) {
            int remainder = array[i] % j; // compute the remainder
            // just did 1000000000 operations
        }
    }

    // Stop timing the parallel portion to calculate how fast it was
    gettimeofday(&end_time, NULL);

    // Compute and print the time used to run all the operation for the parellel portion of the program
    double elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
                          (end_time.tv_usec - start_time.tv_usec) / 1000000.0;
    printf("Elapsed time: %f seconds\n", elapsed_time);

    // Free memory
    free(array);

    return 0;
}
