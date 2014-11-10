#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ROW(i) i/9                      // Code to find ROW of a cell i
#define COL(i) i%9                      // Code to find COL of a cell i
#define CELL(i,j) i*9+j                 // Code to find CELL number from its (ROW,COL) values

#define B_ROW(i) (ROW(i)/3)*3           // Fn to find Block row of a cell
#define B_COL(i) (COL(i)/3)*3           // Fn to find Block col of a cell

#define nROWS 9
#define nCOLS 9
#define INTERVAL 10000                  // Animation interval, Change as you wish 

unsigned long nASSUMPTIONS = 0;         // Keeps track of how many assignments to empty cells are made

typedef struct cell{
    int R, C;
    int A[9];           // Designed for worst case, array to store all possible values
    int N;              // Number of possible values
    int idx;            // Which cell we processed last (TODO : Unnecessary, remove it)
    int isEmpty;        // TODO : Unnecessary, remove it
}Cell, *CellPtr;

// Function to print an array of size N
void printArray(int A[], int N)
{
    int i=0;
    for(i=0; i<N; ++i){
        printf("%d ", A[i]);
    }
    printf("\n");
}

// Function to print the Cell Array, i.e. details of all cells
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

// Function to print the sudoku puzzle
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

// Function to animate the sudoku (Careful : clears all the windows)
void animateSudoku(int S[][nCOLS])
{
    printf("\033c");
    printSudoku(S);
    usleep(INTERVAL);
}

// Function to find all possible values that an empty cell can have.
// S - Input Sudoku
// A - Output Array
// cell_val - The cell being investigated (0-80)
// Returns N - The number of possible values
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

    // Now check in a 3x3 block
    int BLK_R = B_ROW(cell_val);
    int BLK_C = B_COL(cell_val);
    for(i=BLK_R; i<BLK_R+3; ++i){
        for(j=BLK_C; j<BLK_C+3; ++j){
            tmp2 = S[i][j];
            tmp[tmp2] = 0;
        }
    }

    // Now copy all the non-zero elements to A and count it
    for(i=1; i<10; i++){
        if(tmp[i] != 0){
            A[count] = tmp[i];
            ++count;
        }
    }
    
    return count;
}
            
// This function checks if a value inserted in a cell_val violates the Sudoku properties
// Returns 1 if it is Fine, Returns 0 if it violates
int checkViolation(int S[][9], Cell CA[], int cell_val, int key)
{
    int R = CA[cell_val].R; 
    int C = CA[cell_val].C;

    int i, j, tmp2;
    for(i=0; i<9; ++i){         // First check all values in a ROW    
        if(S[R][i]==key)         // if any duplicate number, violated !!!
            return 0;           
    }
    
    for(i=0; i<9; ++i){             // Now check in a column, ie vertical Scanning
        if(S[i][C] == key)         
            return 0;
    }

    // Now check in a 3x3 block
    int BLK_R = B_ROW(cell_val);
    int BLK_C = B_COL(cell_val);
    for(i=BLK_R; i<BLK_R+3; ++i){
        for(j=BLK_C; j<BLK_C+3; ++j){
            if (S[i][j] == key)
                return 0;
        }
    }

    // if no duplicate found, return 1
    return 1;
}


// The main DFS routine which searches through all possible options
// S - Input sudoku
// CA - Input Cell array which contains all informations about the cells
// LIST - Input, A list of empty cells (we need to insert only at empty cells, right?)
// index - input, position in LIST array. Needs to add 1 for every recursive call of DFS
// MaxSize - Size of the LIST, or number of empty cells
// Returns 1 if solution found, else returns 0
int DFS(int S[][9], Cell CA[], int LIST[], int index, int MaxSize)
{
    int backTrace = 1;                                      // flag to decide if backtrack is needed (1) or not(0)
    int status = 0;                                         // Status shows if solution found or not
    
    int cellUT = LIST[index];                               // Take first empty cell
    int nPossibleValues = CA[cellUT].N;                     // Its number of possible values
    int i, testval, vstatus;
    for(i=0; i<nPossibleValues; ++i){
        testval = CA[cellUT].A[i];                          // Take each possible test values
        vstatus = checkViolation(S, CA, cellUT, testval);   // Check if it violates Sudoku
        if(vstatus == 1){                                    // If it is fine
            S[CA[cellUT].R][CA[cellUT].C] = testval;         // Insert the value
            ++nASSUMPTIONS;
            //animateSudoku(S);
            
            if(index == MaxSize-1)                          // Base case, if all cells are filled, return 1
                return 1;                                   // i.e. if cell processed is last one, success !!!
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
        S[CA[LIST[index]].R][CA[LIST[index]].C] = 0;        // If some solution is wrong, backtrack.
//        animateSudoku(S);
        
    return status;
}
