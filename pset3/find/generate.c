/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */
 
#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // check if user provided valid number of arguments
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

    // convert first command line argument from string to int
    int n = atoi(argv[1]);

    // check if user provided second command line argument
    if (argc == 3)
    {
        // if so, generate seed based on this argument
        srand48((long) atoi(argv[2]));
    }
    else
    {
        // if not, generate 'random' seed
        srand48((long) time(NULL));
    }

    // generate n count of 'random' numbers
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}
