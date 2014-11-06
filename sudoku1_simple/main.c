#include "libsudoku.h"
#include <time.h>


int main(int argc, char* argv[])
{
    if(argc != 2){
        printf("Correct Usage : ./a.out sudoku_file\n");
    }

    char input[83];
    char* infile = argv[1];
    FILE *in = fopen(infile, "r");
    if(in == NULL){
        printf("File is not correct. Check the file name");
        exit(1);
    }

    if(fgets(input, 82, in)==NULL){
        printf("Check the contents of the file. \n");
        exit(1);
    }
    
    int Sudoku[9][9];
    Cell CA[81];
    
    int i, r, c, tmp,  nZeroCells=0;
    // Initialize the Sudoku Grid
    for(i=0; i<81; ++i){
        r = ROW(i);
        c = COL(i);
        tmp = input[i]-'0';
        Sudoku[r][c] = tmp;
    }


        // Initialize the CA array (TODO : Above loops can be merged, modify findPossibleValues for 1D array)
    for(i=0; i<81; ++i){
        r = ROW(i);
        c = COL(i);
        tmp = input[i]-'0';
        CA[i].R = r; 
        CA[i].C = c;
        CA[i].N = findPossibleValues(Sudoku, CA[i].A, i);
        CA[i].idx = -1;
        CA[i].isEmpty = CA[i].N>0?1:0;
        if(tmp==0) 
            ++nZeroCells;
    }
    

    int j = 0;
    int ListofEmptyCells[nZeroCells];
    for(i=0; i<81; ++i){
        if(input[i] == '0')
            ListofEmptyCells[j++] = i;
    }

    // Processing starts
    
    clock_t start, end;
    start = clock();
    int status = DFS(Sudoku, CA, ListofEmptyCells, 0, nZeroCells );
    end = clock();

    printf("\033c");
    printSudoku(Sudoku);
    printf(" status: %d\n nAssumptions: %lu\n time: %f\n", status, nASSUMPTIONS, (double)(end-start)/CLOCKS_PER_SEC);
    
}
 
