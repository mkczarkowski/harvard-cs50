#include <cs50.h>
#include <stdio.h>
#include <math.h>

void how_much_coins(float owed);

int main(void)
{
    float owed = -1;
    do
    {
        printf("Oh hai! How much change is owed?\n");
        owed = get_float();
    }
    while (owed < 0);
    how_much_coins(owed);
}

void how_much_coins(float owed)
{
    int owed_in_cents = roundf(owed * 100);
    int coins_to_return = 0;
    int coins_of_type_to_return = 0;
    int coins[4] = {25, 10, 5, 1};

    for (int i = 0; i < sizeof(coins)/sizeof(coins[0]); i++) {
        if (owed_in_cents / coins[i] >= 1.0)
        {
            coins_of_type_to_return  = owed_in_cents / coins[i];
            owed_in_cents = owed_in_cents - coins_of_type_to_return * coins[i];
            coins_to_return += coins_of_type_to_return;
        }
    }
    printf("%i\n", coins_to_return);
}