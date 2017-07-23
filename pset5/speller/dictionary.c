/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// alphabet + apostrophe
#define VALID_CHARACTERS 27

// Trie node
typedef struct node
{
    bool is_word;
    struct node *children[VALID_CHARACTERS];
}
node;

// recursive function for unloading dictionary from memory
void unload_from_bottom(node *node_to_erase, node *backtrack);


// address of dictionary root;
node *head = NULL;

int dictionary_size = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // set cursor on root of the trie
    node *cursor = head;
    int index = 0;
    // iterate over word characters until nul terminator
    while (word[index] != '\0')
    {
        // get children index of character
        int index_of_char = (int) tolower(word[index]) >= 97 ? (int) tolower(word[index]) - 97 : 26;
        // if character not in dictionary consider misspelled
        if (cursor->children[index_of_char] == NULL)
        {
            return false;
        }
        // proceed to layer of a trie
        cursor = cursor->children[index_of_char];
        index++;
    }
    // check if that's the end of valid word
    return cursor->is_word;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *dptr = fopen(dictionary, "r");
    if (dptr == NULL)
    {
        printf("Could not open dictionary.\n");
        return 1;
    }
    
    // root node of dictionary
    node *root = calloc(1, sizeof(node));
    head = root;
    if (root == NULL)
    {
        unload();
        return false;
    }
    // set pointer to first node of a trie
    node *cursor = head;

    for (char c = fgetc(dptr); c != EOF; c = fgetc(dptr))
    {
        if (c != '\n')
        {
            // get children index of character
            int index_of_char = (int) c >= 97 ? (int) c - 97 : 26;
            // if character not yet in a trie, add it
            if (cursor->children[index_of_char] == NULL)
            {
                cursor->children[index_of_char] = calloc(1, sizeof(node));
                if (cursor->children[index_of_char] == NULL)
                {
                    unload();
                    return false;
                }
            }
            // proceed to layer of a trie
            cursor = cursor->children[index_of_char];
        }
        // end of a word reached
        else
        {
            // increment dictionary size
            dictionary_size++;
            // mark current letter as the last one
            cursor->is_word = true;
            // get back to root of a trie
            cursor = head;
        }
    }
    
    // close dictionary file stream
    fclose(dptr);
    
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return dictionary_size;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    unload_from_bottom(head, head);
    // free root node after lower layers were unloaded
    free(head);
    return true;
}

void unload_from_bottom(node *node_to_erase, node *backtrack)
{
        for (int i = 0; i < VALID_CHARACTERS; i++)
        {
            if (node_to_erase->children[i] != NULL)
            {
                // go to lower layer to find the bottom of a trie
                unload_from_bottom(node_to_erase->children[i], node_to_erase);
            }
        }
        
        // free bottom node
        for (int i = 0; i < VALID_CHARACTERS; i++)
        {
            free(node_to_erase->children[i]);
        }
        
        return;
}
