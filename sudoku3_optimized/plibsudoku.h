#ifndef H_SUDOKU
#define H_SUDOKU
#endif

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
#define INTERVAL 5000

typedef unsigned char uchar;
typedef unsigned int uint;

unsigned long nASSUMPTIONS = 0;

typedef struct cell{
//    int R, C;
    uchar A[10];           // Designed for worst case
    uchar N;              // Number of possible values, maximum is 9
    uchar idx;            // Number of possible values right now
//    int isEmpty;        // TODO : Unnecessary, remove it
}Cell, *CellPtr;

void printArray(uchar A[], uchar N)
{
    uchar i=0;
    for(i=0; i<N; ++i){
        printf("%d ", A[i]);
    }
    printf("\n");
}

void printCA(Cell CA[])
{
    uchar i,j;
    printf("i\tR\tC\tN\tidx\tisEmpty\t A\n");
    for(i=0; i<81; i++){
//        printf("%d\t%d\t%d\t%d\t%d\t%d\t" , i, ROW(i), COL(i), CA[i].N, CA[i].idx, CA[i].isEmpty); 
        printf("%d\t%d\t%d\t%d\t%d\t" , i, ROW(i), COL(i), CA[i].N, CA[i].idx); 
        for(j=0; j<CA[i].N; ++j){
            printf("%d ", CA[i].A[j]);
        }
    printf("\n");
    }
}
void printSudoku(uchar S[][nCOLS]) // TODO : Pretty print sudoku
{
    uchar i,j;
    for(i=0; i<nROWS; ++i){
        for(j=0; j<nCOLS; ++j){
            if(S[i][j] == 0)
                printf("  ");
            else
                printf("%d ", S[i][j]);
        }
    printf("\n");
    }
}

void animateSudoku(uchar S[][nCOLS])
{
    printf("\033c");
    printSudoku(S);
    usleep(INTERVAL);
}

uchar findPossibleValues(uchar S[][nCOLS], uchar A[], uchar cell_val)
{
    uchar R = ROW(cell_val);
    uchar C = COL(cell_val);
    uchar count = 0;    

    if (S[R][C]!=0){
        return count;
    }        

    uchar tmp[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    uchar i, j, tmp2;
    for(i=0; i<9; ++i){         // First check all values in a ROW    
        tmp2 = S[R][i];         // Take a number in Sudoku
        tmp[tmp2] = 0;           // Clear it from tmp
    }
    
    for(i=0; i<9; ++i){
        tmp2 = S[i][C];         // Now check in a column, ie vertical scanning
        tmp[tmp2] = 0;
    }

    uchar BLK_R = B_ROW(cell_val);
    uchar BLK_C = B_COL(cell_val);
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
/*
int checkViolation(int S[][9], Cell CA[], int cell_val, int key)
{
    int R = ROW(cell_val);
    int C = COL(cell_val);
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
*/

void updatePossibleValues(Cell CA[], uchar cell_val, uchar given_val)
{
    uchar R = ROW(cell_val);
    uchar C = COL(cell_val);

    //int tmp[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    char i, j, k, tmp,  tmp2, n;
    for(i=0; i<9; ++i){         // First check all values in a ROW    
        tmp = R*9+i;
        n = CA[tmp].N;
        for(j=0; j<n; ++j){         //     
            if(CA[tmp].A[j] == given_val){        // Take a number in Sudoku
                CA[tmp].A[j] = 0;           // Clear it from tmp
                --CA[tmp].idx;
                break;
            }
        }
    }
    
    for(i=0; i<9; ++i){
        tmp = i*9+C;
        n = CA[tmp].N;
        for(j=0; j<n; ++j){
            if(CA[tmp].A[j] == given_val){
                CA[tmp].A[j] = 0;         // Now check in a column, ie vertical scanning
                --CA[tmp].idx;
                break;
            }
        }
    }

    uchar BLK_R = B_ROW(cell_val);
    uchar BLK_C = B_COL(cell_val);
    for(i=BLK_R; i<BLK_R+3; ++i){
        for(j=BLK_C; j<BLK_C+3; ++j){
            tmp = i*9+j;
            n = CA[tmp].N;
            for(k=0; k<n; ++k){         //     
                if(CA[tmp].A[k] == given_val){        // Take a number in Sudoku
                    CA[tmp].A[k] = 0;           // Clear it from tmp
                    --CA[tmp].idx;
                    break;
                }
            }
        }
    }

}


//Implement the partition function
//Each time choose the pivot as the 
// left most element and partition the 
// array based on this pivot
//  Return the index of Pivot
uchar Partition(uchar A[], Cell CA[], char l, char r){
    uchar pivot = A[l], pivotN = CA[pivot].idx; 
    char wall = l;
    uchar temp,i; 
    for (i = l+1; i <= r; ++i)
        if(CA[A[i]].idx < pivotN) {
            ++wall; 
            temp = A[i];
            A[i] = A[wall];
            A[wall] = temp;
        }
    temp = A[l];
    A[l] = A[wall];
    A[wall] = temp;
    //printf("%d\n",wall);
    return wall; 
}


//Write the quicksort recursive calls
//This function performs  the quicksort
void QuickSort(uchar A[], Cell CA[], char l, char r)
{
    if(l<r) {
        char pivot_pos = Partition(A, CA, l, r);
        QuickSort(A,CA,l,pivot_pos-1); 
        QuickSort(A,CA,pivot_pos+1,r); 
    }
}

uchar DFS(uchar S[][9], Cell CA[], uchar LIST[], uchar MaxSize)
{
    
    uchar backTrace = 1;
    uchar status = 0;

    uchar cellUT = LIST[0];                               // Cell Under Test
    uchar R = ROW(cellUT);
    uchar C = COL(cellUT);
    uchar nPossibleValues = CA[cellUT].N;                     // Its number of possible values
    uchar i, currSize, vstatus;
    uchar testval;
    for(i=0; i<nPossibleValues; ++i){
        testval = CA[cellUT].A[i];                          // Take each possible test values
        if (testval == 0) 
            continue;
        S[R][C] = testval;            // assign it.
        ++nASSUMPTIONS;
            //animateSudoku(S);
        currSize = MaxSize-1;
        if(currSize == 0)
            return 1;                                   // if cell processed is last one, success !!!
        else{
            Cell CA2[81];
            uchar LIST2[MaxSize]; 
            memcpy(CA2, CA, 81*sizeof(Cell));
            updatePossibleValues(CA2, cellUT, testval);
            memcpy(LIST2, &LIST[1], currSize*sizeof(uchar)); 
            QuickSort(LIST2, CA2, 0, currSize-1); 
            //printArray(LIST2, currSize);
            if(CA2[LIST2[0]].idx>0){
                status = DFS(S, CA2, LIST2, currSize); // Otherwise, RUN DFS on next empty cell
                if(status == 1){
                    backTrace = 0;
                    break;                      // If that is the output, don't inspect other elements
                }
             }
        }
    }
    
    if(backTrace){
        S[R][C] = 0;
    }
//        animateSudoku(S);
        
    return status;
}


