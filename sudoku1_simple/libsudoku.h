#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ROW(i) i/9
#define COL(i) i%9
#define CELL(i,j) i*9+j

#define B_ROW(i) (ROW(i)/3)*3
#define B_COL(i) (COL(i)/3)*3
//#define B_ROWk`

#define nROWS 9
#define nCOLS 9
#define INTERVAL 10000

unsigned long nASSUMPTIONS = 0;

typedef struct cell{
    int R, C;
    int A[9];           // Designed for worst case
    int N;              // Number of possible values
    int idx;            // Which cell we processed last (TODO : Unnecessary, remove it)
    int isEmpty;        // TODO : Unnecessary, remove it
}Cell, *CellPtr;

void printArray(int A[], int N)
{
    int i=0;
    for(i=0; i<N; ++i){
        printf("%d ", A[i]);
    }
    printf("\n");
}

void printCA(Cell CA[])
{
    int i,j;
    printf("i\tR\tC\tN\tidx\tisEmpty\t A\n");
    for(i=0; i<81; i++){
        printf("%d\t%d\t%d\t%d\t%d\t%d\t" , i, CA[i].R, CA[i].C, CA[i].N, CA[i].idx, CA[i].isEmpty); 
        for(j=0; j<CA[i].N; ++j){
            printf("%d ", CA[i].A[j]);
        }
    printf("\n");
    }
}

void printSudoku(int S[][nCOLS]) // TODO : Pretty print sudoku
{
    int i,j;
    for(i=0; i<nROWS; ++i){
        if(i==3 || i==6)
            printf("- - - + - - - + - - -\n");
        for(j=0; j<nCOLS; ++j){
            if (j==3 || j==6)
                printf("| ");
            if(S[i][j] == 0)
                printf("  ");
            else
                printf("%d ", S[i][j]);
        }
    printf("\n");
    }
}

void animateSudoku(int S[][nCOLS])
{
    printf("\033c");
    printSudoku(S);
    usleep(INTERVAL);
}

int findPossibleValues(int S[][nCOLS], int A[], int cell_val)
{
    int R = ROW(cell_val);
    int C = COL(cell_val);
    int count = 0;    

    if (S[R][C]!=0){
        return count;
    }        

    int tmp[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int i, j, tmp2;
    for(i=0; i<9; ++i){         // First check all values in a ROW    
        tmp2 = S[R][i];         // Take a number in Sudoku
        tmp[tmp2] = 0;           // Clear it from tmp
    }
    
    for(i=0; i<9; ++i){
        tmp2 = S[i][C];         // Now check in a column, ie vertical scanning
        tmp[tmp2] = 0;
    }

    int BLK_R = B_ROW(cell_val);
    int BLK_C = B_COL(cell_val);
    for(i=BLK_R; i<BLK_R+3; ++i){
        for(j=BLK_C; j<BLK_C+3; ++j){
            tmp2 = S[i][j];
            tmp[tmp2] = 0;
        }
    }

    for(i=1; i<10; i++){
        if(tmp[i] != 0){
            A[count] = tmp[i];
            ++count;
        }
    }
    
    return count;
}
            
// This function checks if a value inserted in a cell_val violates the Sudoku properties
// Returns 1 if it is Fine, Else it returns 0
int checkViolation(int S[][9], Cell CA[], int cell_val, int key)
{
    int R = CA[cell_val].R; 
    int C = CA[cell_val].C;
    //int tmp[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int i, j, tmp2;
    for(i=0; i<9; ++i){         // First check all values in a ROW    
        if(S[R][i]==key)         // Take a number in Sudoku
            return 0;           // Clear it from tmp
    }
    
    for(i=0; i<9; ++i){
        if(S[i][C] == key)         // Now check in a column, ie vertical scanning
            return 0;
    }

    int BLK_R = B_ROW(cell_val);
    int BLK_C = B_COL(cell_val);
    for(i=BLK_R; i<BLK_R+3; ++i){
        for(j=BLK_C; j<BLK_C+3; ++j){
            if (S[i][j] == key)
                return 0;
        }
    }

    return 1;
}


int DFS(int S[][9], Cell CA[], int LIST[], int index, int MaxSize)
{
    int backTrace = 1;
    int status = 0;
    
    int cellUT = LIST[index];                               // Cell Under Test
    int nPossibleValues = CA[cellUT].N;                     // Its number of possible values
    int i, testval, vstatus;
    for(i=0; i<nPossibleValues; ++i){
        testval = CA[cellUT].A[i];                          // Take each possible test values
        vstatus = checkViolation(S, CA, cellUT, testval);   // Check if it violates Sudoku
        if(vstatus == 1){                                    // If it is fine
            S[CA[cellUT].R][CA[cellUT].C] = testval;         // Insert the value
            ++nASSUMPTIONS;
            //animateSudoku(S);
            
            if(index == MaxSize-1)
                return 1;                                   // if cell processed is last one, success !!!
            else{
                status = DFS(S, CA, LIST, index+1, MaxSize); // Otherwise, RUN DFS on next empty cell
                if(status == 1){
                    backTrace = 0;
                    break;                      // If that is the output, don't inspect other elements
                }
            }
        }
    }
    
    if(backTrace)
        S[CA[LIST[index]].R][CA[LIST[index]].C] = 0;
//        animateSudoku(S);
        
    return status;
}
