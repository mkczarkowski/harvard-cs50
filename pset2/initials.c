#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string name = get_string();
    // assign first letter of passed name to array of initials
    char initials[4] = { toupper(name[0]) };
    // keep track of which index is next
    int initialsIndex = 1;

    for (int i = 1, n = strlen(name); i < n; i++)
    {
        // check if i'th character of name is whitespace
        if (name[i] == ' ')
        {
            // pass character that proceeds it to array of initials
            initials[initialsIndex] = toupper(name[i + 1]);
            initialsIndex++;
        }
    }
    // assign nul terminator to last index
    initials[3] = '\0';
    printf("%s\n", initials);
}