#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char plainToCipher(char toCipher, int key);

int main(int argc, string argv[])
{
    // check if user provided desired amount of 2 arguments
    if (argc != 2)
    {
        // if no, print error and return value that is not 0
        printf("Please provide only one argument with a keyword for your cipher.\n");
        return 1;
    }
    else
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isdigit(argv[1][i]))
            {
                printf("Please provide a keyword without digits.");
                return 1;
            }
        }
        // get cipher key provided by user
        printf("plaintext: ");
        string plaintext = get_string();
        int key = 0;
        int keyIndexTracker = 0;
        // calculate input length and declare output of the same size
        int plaintextLen = strlen(plaintext);
        char ciphertext[plaintextLen + 1];
        for (int i = 0; i < plaintextLen; i++)
        {
            // check if keyword index tracker is equal to keyword length
            if (keyIndexTracker == strlen(argv[1]))
            {
                // if so, reset tracker
                keyIndexTracker = 0;
            }
            // check if i'th character is upper alphabetical character
            if (plaintext[i] >= 65 && plaintext[i] <= 90)
            {
                // if so, calculate numerical key and increment tracker
                key = toupper(argv[1][keyIndexTracker]) - 65;
                keyIndexTracker++;
            }
            // check if i'th character is lower alphabetical character
            else if (plaintext[i] >= 97 && plaintext[i] <= 122)
            {
                // if so, calculate numerical key and increment tracker
                key = tolower(argv[1][keyIndexTracker]) - 97;
                keyIndexTracker++;
            }
            // get ciphered character
            ciphertext[i] = plainToCipher(plaintext[i], key);
            // reset key value to 0 in case next character is non-alphabetical
            key = 0;
        }
        // mark the end of cipher with nul terminator
        ciphertext[plaintextLen] = '\0';
        printf("ciphertext: %s\n", ciphertext);
    }
}

char plainToCipher(char toCipher, int key)
{
    // check if character + key is in range of ascii values reserved for alphabet letters
    if ((toCipher >= 65 && toCipher + key < 90) ||
        (toCipher >= 97 && toCipher + key < 123))
    {
        // if so, just add key value to character
        return toCipher + key;
    }
    // check if character is in range of ascii alphabet letters
    else if ((toCipher >= 65 && toCipher < 90) ||
             (toCipher >= 97 && toCipher < 123))
    {
        // if so, calculate ciphered character
        return toCipher < 90 ? 65 + (key - (91 - toCipher)) : 97 + (key - (123 - toCipher));
    }
    else
    {
        // character is not a letter from alphabet, leave it as it is
        return toCipher;
    }
}