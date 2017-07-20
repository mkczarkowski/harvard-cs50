#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("Minutes: ");
    int mins = get_int();
    printf("Bottles: %i\n", mins * 12);
}