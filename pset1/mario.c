#include <cs50.h>
#include <stdio.h>

void build_pyramid(int height);

int main(void)
{
    int height = -1;
    do
    {
        printf("Height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);
    build_pyramid(height);
}

void build_pyramid(int height)
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - 1 - i; j++)
        {
            printf(" ");
        }

        for (int k = 0; k < i + 2; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}