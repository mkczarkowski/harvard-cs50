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
        printf("Ceasar demands only one argument, obey citizen ;).\n");
        return 1;
    }
    else
    {
        // get cipher key provided by user
        int key = atoi(argv[1]) % 26;
        printf("plaintext: ");
        string plaintext = get_string();

        // calculate input length and declare output of the same size
        int plaintextLen = strlen(plaintext);
        char ciphertext[plaintextLen + 1];

        for (int i = 0; i < plaintextLen; i++)
        {
            // get ciphered character for i'th plain character
            ciphertext[i] = plainToCipher(plaintext[i], key);
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
        return toCipher < 90 ? 65 + (key - (90 - toCipher)) : 97 + (key - (123 - toCipher));
    }
    else
    {
        // character is not a letter from alphabet, leave it as it is
        return toCipher;
    }
}