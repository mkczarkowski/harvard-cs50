/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

bool binary_search(int value, int values[], int left, int right);

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    bool is_found = false;
    
    if (n <= 0)
    {
        return false;
    }
    else
    {
            is_found = binary_search(value, values, 0, n - 1);
    }
    
    return is_found;
}

/**
 * Sorts array of n values with insertion algorithm.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int to_swap;
    
    for (int i = 0; i < n; i++)
    {
        int j = i;
        // swap values until j-1'th is bigger than j'th
        while (j > 0 && values[j - 1] > values[j])
        {
            to_swap = values[j - 1];
            values[j - 1] = values[j];
            values[j] = to_swap;
        }
    }
    
    return;
}

bool binary_search(int value, int values[], int left, int right)
{
    // get index in the middle of analyzed part
    int middle = (left + right) / 2;
    
    // check if number we look for is in the middle
    if (value == values[middle])
    {
        return true;
    }
    // check if end of array is reached
    else if (right == middle)
    {
        return false;
    }
    else 
    {
        // check if value is bigger then middle one
        if (value > values[middle])
        {
            return binary_search(value, values, middle + 1, right);
        }
        else
        {
            return binary_search(value, values, left, right / 2);
        }
    }
}