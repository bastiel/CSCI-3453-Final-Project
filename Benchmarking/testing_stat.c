/*
When executing this code, check both terminal and debug console
Terminal will show total time of program execution
Debug Console will show the threads being created and exiting
This sample code tests the system call stat()

DELETE BELOW AFTER TESTING
So far on linux, running this code with 100,000 iterations and 16 threads takes 0.205219259 seconds
With 10,000 iterations and 16 threads, it takes 0.030679869 seconds

As expected, less iterations takes less time

However, when swithing the thread count from 16 to 1,
100,000 itertions: 0.032978139 seconds
10,000 iterations: 0.003351668 seconds
*/

#include <stdio.h>
#include <pthread.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>

#define NUM_THREADS 1
#define ITERATIONS 100000

void* benchmark(void* arg) {
    struct stat sb;   //Declare a variable to store file status.
    
    //Loop to perform the system call ITERATIONS number of times.
    for (int i = 0; i < ITERATIONS; i++) {
        stat("test_file.txt", &sb); //Perform the stat() system call on test_file.txt.
    }
    
    return NULL; //Return null as the thread function is void.
}

int main() {
    pthread_t threads[NUM_THREADS];  //Array of pthread_t to hold thread identifiers.
    struct timespec start, end;      //Variables to store the start and end times for benchmarking.

    //Get the start time for the benchmark (in nanoseconds).
    clock_gettime(CLOCK_MONOTONIC, &start);

    //Create NUM_THREADS threads to run the benchmark function.
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, benchmark, NULL); //Create each thread.
    }
    
    //Wait for all threads to finish execution.
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL); //Join each thread, ensuring they all complete.
    }

    //Get the end time after all threads have finished.
    clock_gettime(CLOCK_MONOTONIC, &end);

    //Calculate the total time taken for the benchmark in seconds.
    double time_taken = (end.tv_sec - start.tv_sec) +
                        (end.tv_nsec - start.tv_nsec) / 1e9;
    
    //Print the total time taken with the specified number of threads.
    printf("Total time with %d threads: %.9f seconds\n", NUM_THREADS, time_taken);

    return 0; //Return 0 to indicate successful execution.
}