/**
 * Resizes a BMP by given factor
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int getPadding(int width);
void writePadding(FILE *file, int padding);

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // resize scale
    int n = atoi(argv[1]);
    
    if (n < 1 || n > 100)
    {
        fprintf(stderr, "n must be a positive integer less than or equal to 100.\n");
        return 1; 
    }
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    // width and height of infile
    LONG originalWidth = bi.biWidth;
    LONG originalHeight = bi.biHeight;
    
    // width and height of outfile
    bi.biWidth *= n;
    bi.biHeight *= n;
    
    // determine padding for infile and outfile
    int originalPadding = getPadding(originalWidth);
    int padding = getPadding(bi.biWidth);

    // resize image and file size
    // sprawdz o co chodzi z 3
    bi.biSizeImage = (bi.biWidth * sizeof(RGBTRIPLE) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // array to duplicate rows vertically
    RGBTRIPLE row[bi.biWidth];

    // iterate over infile's scanlines
    for (int i = 0; i < abs(originalHeight); i++)
    {
        
        // iterate over pixels in scanline
        for (int j = 0; j < originalWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
            // resize horizontally
            for (int k = 0; k < n; k++)
            {
                row[(j * n) + k] = triple;
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }
        
        // write outfile padding for current row
        writePadding(outptr, padding);
        
        // resize vertically
        for (int j = 0; j < n - 1; j++)
        {
            fwrite(&row, sizeof(row), 1, outptr);
            writePadding(outptr, padding);
        }
        
        // skip over infile padding, if any
        fseek(inptr, originalPadding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

int getPadding(LONG width) 
{
    return (4 - (width * sizeof(RGBTRIPLE)) % 4) % 4;
}

void writePadding(FILE *file, int padding)
{
    for (int i = 0; i < padding; i++)
    {
        fputc(0x00, file);
    }
}