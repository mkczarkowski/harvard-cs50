#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

// size of data block
#define BLOCK 512

bool checkHeader(uint8_t buffer[BLOCK]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover forensic\n");
        return 1;
    }

    // remember filename
    char *forensic = argv[1];

    // open forensic image
    FILE *inptr = fopen(forensic, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", forensic);
        return 2;
    }

    // buffer for data blocks
    uint8_t buffer[BLOCK];

    // expected number of bytes to read from input
    int readVal = 512;

    // track file names
    int fileNameCounter = 0;

    // first jpg encounter
    bool startOfJpgs = false;

    // next jpg encounter
    bool newJpg = false;

    // eof encounter
    bool eof = false;

    // look for first jpg
    while (!startOfJpgs)
    {
        fread(&buffer, 1, BLOCK, inptr);

        startOfJpgs = checkHeader(buffer);
    }

    // generate new jpg until eof
    while (!eof) {
        // generate new .jpg file
        char *outfile = malloc(sizeof(char) * 3 + 1);
        sprintf(outfile, "%03i.jpg", fileNameCounter);
        FILE *outptr = fopen(outfile, "w");

        newJpg = false;

        // write until newJpg/eof is found
        while (!newJpg && !eof)
        {
            fwrite(&buffer, BLOCK, 1, outptr);
            readVal = fread(&buffer, 1, BLOCK, inptr);

            newJpg = checkHeader(buffer);
            eof = readVal != BLOCK ? true : false;
        }

        // close outfile
        fclose(outptr);

        // free memory for outfile name
        free(outfile);

        // next jpg file name
        fileNameCounter++;
    }

    // close infile
    fclose(inptr);
}

bool checkHeader(uint8_t buffer[BLOCK])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}